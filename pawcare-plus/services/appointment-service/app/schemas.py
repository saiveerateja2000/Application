from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import AppointmentStatus

class AppointmentBase(BaseModel):
    pet_id: int
    appointment_date: datetime
    doctor_name: str
    reason: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.REQUESTED

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: AppointmentStatus