from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, models, schemas
from ..database import get_db
import httpx
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

NOTIFICATION_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8003")

async def notify_status_change(appointment_id: int, old_status: str, new_status: str):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{NOTIFICATION_URL}/notifications/", json={
                "appointment_id": appointment_id,
                "old_status": old_status,
                "new_status": new_status
            })
        except Exception as e:
            logger.error(f"Failed to notify status change: {e}")

@router.post("/appointments/", response_model=schemas.Appointment)
async def create_appointment(appointment: schemas.AppointmentCreate, db: AsyncSession = Depends(get_db)):
    db_appointment = await crud.create_appointment(db=db, appointment=appointment)
    return db_appointment

@router.get("/appointments/", response_model=List[schemas.Appointment])
async def read_appointments(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    appointments = await crud.get_appointments(db, skip=skip, limit=limit)
    return appointments

@router.get("/appointments/{appointment_id}", response_model=schemas.Appointment)
async def read_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    db_appointment = await crud.get_appointment(db, appointment_id=appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment

@router.put("/appointments/{appointment_id}/status", response_model=schemas.Appointment)
async def update_appointment_status(appointment_id: int, status_update: schemas.StatusUpdate, db: AsyncSession = Depends(get_db)):
    try:
        db_appointment, old_status = await crud.update_appointment_status(db, appointment_id=appointment_id, status=status_update.status)
        if db_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        # Notify status change
        await notify_status_change(appointment_id, old_status.value, status_update.status.value)
        return db_appointment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))