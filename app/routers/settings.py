import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import ProfileUpdate, PasswordChange, PreferencesUpdate, UserOut
from app.security import get_current_user, verify_password, hash_password

router = APIRouter(prefix="/settings", tags=["Module 27 - Profile & Settings"])

@router.get("/profile", response_model=UserOut)
def profile(user: User = Depends(get_current_user)):
    return user

@router.patch("/profile", response_model=UserOut)
def update_profile(data: ProfileUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.full_name = data.full_name
    db.commit(); db.refresh(user); return user

@router.post("/change-password")
def change_password(data: PasswordChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(400, "Current password is incorrect")
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.get("/preferences")
def preferences(user: User = Depends(get_current_user)):
    try: return json.loads(user.notification_preferences or "{}")
    except json.JSONDecodeError: return {"email": True, "in_app": True}

@router.put("/preferences")
def update_preferences(data: PreferencesUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user.notification_preferences = json.dumps(data.model_dump())
    db.commit()
    return data.model_dump()
