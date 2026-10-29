from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Onboarding, User
from app.schemas import OnboardingCreate, StatusUpdate
from app.security import get_current_user, require_roles, require_employee_id

router = APIRouter(prefix="/onboarding", tags=["Module 21 - Onboarding"])

@router.post("", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def create_task(data: OnboardingCreate, db: Session = Depends(get_db)):
    item = Onboarding(**data.model_dump(), status="PENDING")
    db.add(item); db.commit(); db.refresh(item); return item

@router.get("")
def list_tasks(employee_id: int | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    target = employee_id or user.employee_id
    if target is None and user.role not in {"ADMIN", "HR"}:
        raise HTTPException(400, "Your account is not linked to an employee_id")
    if target is not None: require_employee_id(user, target)
    q = db.query(Onboarding)
    if target is not None: q = q.filter(Onboarding.employee_id == target)
    return q.order_by(Onboarding.id.desc()).all()

@router.patch("/{item_id}/status")
def update_status(item_id: int, data: StatusUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.get(Onboarding, item_id)
    if not item: raise HTTPException(404, "Onboarding task not found")
    require_employee_id(user, item.employee_id)
    item.status = data.status; db.commit(); db.refresh(item); return item

@router.get("/progress/{employee_id}")
def progress(employee_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    require_employee_id(user, employee_id)
    items = db.query(Onboarding).filter(Onboarding.employee_id == employee_id).all()
    total = len(items); completed = sum(x.status == "COMPLETED" for x in items)
    return {"employee_id": employee_id, "total": total, "completed": completed,
            "pending": total-completed, "progress_percent": round(completed*100/total) if total else 0}
