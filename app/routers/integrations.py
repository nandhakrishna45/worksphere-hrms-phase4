import csv, io, smtplib
from email.message import EmailMessage
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.config import settings
from app.database import get_db
from app.models import Onboarding, Resignation, Announcement, Task, Feedback, User
from app.security import get_current_user, require_roles

router = APIRouter(prefix="/integrations", tags=["Module 25 - Integrations"])
RESOURCES = {
    "onboarding": Onboarding,
    "resignations": Resignation,
    "announcements": Announcement,
    "tasks": Task,
    "feedback": Feedback,
}

@router.get("/calendar-status")
def calendar_status(user: User = Depends(get_current_user)):
    return {"provider": "Google Calendar", "configured": False,
            "message": "OAuth client credentials and callback flow are not configured. This endpoint is a readiness placeholder."}

@router.post("/email-test", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def email_test(to_email: str, user: User = Depends(get_current_user)):
    if not all([settings.smtp_host, settings.smtp_from_email]):
        raise HTTPException(503, "SMTP is not configured. Set SMTP_HOST and SMTP_FROM_EMAIL in .env.")
    msg = EmailMessage()
    msg["Subject"] = "WorkSphere HRMS email integration test"
    msg["From"] = settings.smtp_from_email
    msg["To"] = to_email
    msg.set_content("This is a test notification from WorkSphere HRMS.")
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            if settings.smtp_use_tls: server.starttls()
            if settings.smtp_username and settings.smtp_password:
                server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
    except Exception as exc:
        raise HTTPException(502, f"Email delivery failed: {type(exc).__name__}")
    return {"message": "Test email sent"}

@router.get("/export/{resource}.csv", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def export_csv(resource: str, db: Session = Depends(get_db)):
    model = RESOURCES.get(resource)
    if not model: raise HTTPException(404, "Unsupported export resource")
    rows = db.query(model).all()
    fields = list(model.__table__.columns.keys())
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(fields)
    for row in rows:
        writer.writerow([str(getattr(row, field, "")) if getattr(row, field, None) is not None else "" for field in fields])
    return StreamingResponse(iter([stream.getvalue()]), media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{resource}.csv"'})

@router.get("/export/{resource}.pdf", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def export_pdf(resource: str, db: Session = Depends(get_db)):
    model = RESOURCES.get(resource)
    if not model: raise HTTPException(404, "Unsupported export resource")
    rows = db.query(model).all()
    fields = list(model.__table__.columns.keys())
    buf = io.BytesIO()
    pdf = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    y = height - 45
    pdf.setFont("Helvetica-Bold", 14); pdf.drawString(40, y, f"WorkSphere - {resource.title()} Report")
    y -= 25; pdf.setFont("Helvetica", 7)
    pdf.drawString(40, y, " | ".join(fields)[:150]); y -= 15
    for row in rows:
        line = " | ".join(str(getattr(row, f, "")) for f in fields)
        pdf.drawString(40, y, line[:150]); y -= 12
        if y < 45:
            pdf.showPage(); y = height - 45; pdf.setFont("Helvetica", 7)
    pdf.save(); buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{resource}.pdf"'})
