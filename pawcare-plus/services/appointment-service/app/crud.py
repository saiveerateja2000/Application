from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

VALID_TRANSITIONS = {
    models.AppointmentStatus.REQUESTED: [models.AppointmentStatus.CONFIRMED, models.AppointmentStatus.CANCELLED],
    models.AppointmentStatus.CONFIRMED: [models.AppointmentStatus.IN_PROGRESS, models.AppointmentStatus.CANCELLED],
    models.AppointmentStatus.IN_PROGRESS: [models.AppointmentStatus.COMPLETED, models.AppointmentStatus.CANCELLED],
    models.AppointmentStatus.COMPLETED: [],
    models.AppointmentStatus.CANCELLED: []
}

async def get_appointment(db: AsyncSession, appointment_id: int):
    result = await db.execute(select(models.Appointment).where(models.Appointment.id == appointment_id))
    return result.scalars().first()

async def get_appointments(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Appointment).offset(skip).limit(limit))
    return result.scalars().all()

async def create_appointment(db: AsyncSession, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    return db_appointment

async def update_appointment_status(db: AsyncSession, appointment_id: int, status: models.AppointmentStatus):
    db_appointment = await get_appointment(db, appointment_id)
    if db_appointment:
        if status not in VALID_TRANSITIONS[db_appointment.status]:
            raise ValueError(f"Invalid status transition from {db_appointment.status} to {status}")
        old_status = db_appointment.status
        db_appointment.status = status
        await db.commit()
        await db.refresh(db_appointment)
        return db_appointment, old_status
    return None, None