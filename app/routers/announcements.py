from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Announcement, User
from app.schemas import AnnouncementCreate
from app.security import get_current_user, require_roles

router = APIRouter(prefix="/announcements", tags=["Module 23 - Announcements"])

@router.post("", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def create(data: AnnouncementCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = Announcement(**data.model_dump(), created_by=user.id)
    db.add(item); db.commit(); db.refresh(item); return item

@router.get("")
def list_all(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).all()

@router.get("/{announcement_id}")
def detail(announcement_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.get(Announcement, announcement_id)
    if not item: raise HTTPException(404, "Announcement not found")
    return item

@router.delete("/{announcement_id}", dependencies=[Depends(require_roles("ADMIN", "HR"))])
def delete(announcement_id: int, db: Session = Depends(get_db)):
    item = db.get(Announcement, announcement_id)
    if not item: raise HTTPException(404, "Announcement not found")
    db.delete(item); db.commit(); return {"message": "Announcement deleted"}
