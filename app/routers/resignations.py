from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Resignation, User
from app.schemas import ResignationCreate, ResignationDecision
from app.security import get_current_user, require_roles, require_employee_id

router = APIRouter(prefix="/resignations", tags=["Module 22 - Resignations"])

@router.post("")
def submit(data: ResignationCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.employee_id is None: raise HTTPException(400, "Your account is not linked to an employee_id")
    item = Resignation(employee_id=user.employee_id, reason=data.reason, notice_period=data.notice_period)
    db.add(item); db.commit(); db.refresh(item); return item

@router.get("")
def list_resignations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Resignation)
    if user.role not in {"ADMIN", "HR"}:
        if user.employee_id is None: return []
        q = q.filter(Resignation.employee_id == user.employee_id)
    return q.order_by(Resignation.created_at.desc()).all()

@router.patch("/{resignation_id}/decision", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def decision(resignation_id: int, data: ResignationDecision, db: Session = Depends(get_db)):
    item = db.get(Resignation, resignation_id)
    if not item: raise HTTPException(404, "Resignation not found")
    item.status = data.status; db.commit(); db.refresh(item); return item
