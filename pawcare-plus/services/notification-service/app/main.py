from fastapi import FastAPI
from .schemas import NotificationCreate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0")

@app.post("/notifications/")
async def create_notification(notification: NotificationCreate):
    logger.info(f"Notification: Appointment {notification.appointment_id} status changed from {notification.old_status} to {notification.new_status}")
    # In a real app, send email, SMS, etc.
    return {"message": "Notification logged"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Notification Service API"}