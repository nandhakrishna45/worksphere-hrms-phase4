from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=10, max_length=128)
    role: str = "EMPLOYEE"
    employee_id: int | None = Field(default=None, ge=1)
    @field_validator("role")
    @classmethod
    def valid_role(cls, v):
        v = v.upper()
        if v not in {"EMPLOYEE", "HR", "ADMIN"}:
            raise ValueError("role must be EMPLOYEE, HR, or ADMIN")
        return v

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    employee_id: int | None
    model_config = ConfigDict(from_attributes=True)

class OnboardingCreate(BaseModel):
    employee_id: int = Field(ge=1)
    task_name: str = Field(min_length=2, max_length=200)
    due_date: date | None = None

class StatusUpdate(BaseModel):
    status: str
    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        v = v.upper()
        if v not in {"PENDING", "COMPLETED"}:
            raise ValueError("status must be PENDING or COMPLETED")
        return v

class ResignationCreate(BaseModel):
    reason: str = Field(min_length=5, max_length=5000)
    notice_period: int = Field(ge=0, le=365)

class ResignationDecision(BaseModel):
    status: str
    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        v = v.upper()
        if v not in {"APPROVED", "REJECTED"}:
            raise ValueError("status must be APPROVED or REJECTED")
        return v

class AnnouncementCreate(BaseModel):
    title: str = Field(min_length=2, max_length=220)
    message: str = Field(min_length=2, max_length=10000)

class TaskCreate(BaseModel):
    assigned_to: int = Field(ge=1)
    title: str = Field(min_length=2, max_length=220)
    description: str = Field(default="", max_length=10000)
    due_date: date | None = None

class FeedbackCreate(BaseModel):
    message: str = Field(min_length=2, max_length=5000)
    rating: int = Field(ge=1, le=5)

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=160)

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=10, max_length=128)

class PreferencesUpdate(BaseModel):
    email: bool = True
    in_app: bool = True
