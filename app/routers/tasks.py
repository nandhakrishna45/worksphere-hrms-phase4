from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task, User
from app.schemas import TaskCreate, StatusUpdate
from app.security import get_current_user, require_roles

router = APIRouter(prefix="/tasks", tags=["Module 24 - Tasks"])

@router.post("", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def create(data: TaskCreate, db: Session = Depends(get_db)):
    item = Task(**data.model_dump(), status="PENDING")
    db.add(item); db.commit(); db.refresh(item); return item

@router.get("")
def list_tasks(assigned_to: int | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role not in {"ADMIN", "HR"}:
        if user.employee_id is None: return []
        assigned_to = user.employee_id
    q = db.query(Task)
    if assigned_to is not None: q = q.filter(Task.assigned_to == assigned_to)
    return q.order_by(Task.id.desc()).all()

@router.patch("/{task_id}/status")
def update_status(task_id: int, data: StatusUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.get(Task, task_id)
    if not item: raise HTTPException(404, "Task not found")
    if user.role not in {"ADMIN", "HR"} and item.assigned_to != user.employee_id:
        raise HTTPException(403, "You can only update tasks assigned to you")
    item.status = data.status; db.commit(); db.refresh(item); return item

@router.delete("/{task_id}", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def delete(task_id: int, db: Session = Depends(get_db)):
    item = db.get(Task, task_id)
    if not item: raise HTTPException(404, "Task not found")
    db.delete(item); db.commit(); return {"message": "Task deleted"}
