from pydantic import BaseModel

class NotificationCreate(BaseModel):
    appointment_id: int
    old_status: str
    new_status: str