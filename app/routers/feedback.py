from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Feedback, User
from app.schemas import FeedbackCreate
from app.security import get_current_user, require_roles

router = APIRouter(prefix="/feedback", tags=["Module 26 - Feedback"])

@router.post("")
def submit(data: FeedbackCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.employee_id is None: raise HTTPException(400, "Your account is not linked to an employee_id")
    item = Feedback(employee_id=user.employee_id, **data.model_dump())
    db.add(item); db.commit(); db.refresh(item); return item

@router.get("", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def list_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
