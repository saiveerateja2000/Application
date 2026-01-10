from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(select(models.Owner).where(models.Owner.id == owner_id))
    return result.scalars().first()

async def get_owners(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Owner).offset(skip).limit(limit))
    return result.scalars().all()

async def create_owner(db: AsyncSession, owner: schemas.OwnerCreate):
    db_owner = models.Owner(**owner.model_dump())
    db.add(db_owner)
    await db.commit()
    await db.refresh(db_owner)
    return db_owner

async def update_owner(db: AsyncSession, owner_id: int, owner: schemas.OwnerCreate):
    db_owner = await get_owner(db, owner_id)
    if db_owner:
        for key, value in owner.model_dump().items():
            setattr(db_owner, key, value)
        await db.commit()
        await db.refresh(db_owner)
    return db_owner

async def delete_owner(db: AsyncSession, owner_id: int):
    db_owner = await get_owner(db, owner_id)
    if db_owner:
        await db.delete(db_owner)
        await db.commit()
    return db_owner

async def get_pet(db: AsyncSession, pet_id: int):
    result = await db.execute(select(models.Pet).where(models.Pet.id == pet_id))
    return result.scalars().first()

async def get_pets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Pet).offset(skip).limit(limit))
    return result.scalars().all()

async def create_pet(db: AsyncSession, pet: schemas.PetCreate):
    db_pet = models.Pet(**pet.model_dump())
    db.add(db_pet)
    await db.commit()
    await db.refresh(db_pet)
    return db_pet

async def update_pet(db: AsyncSession, pet_id: int, pet: schemas.PetCreate):
    db_pet = await get_pet(db, pet_id)
    if db_pet:
        for key, value in pet.model_dump().items():
            setattr(db_pet, key, value)
        await db.commit()
        await db.refresh(db_pet)
    return db_pet

async def delete_pet(db: AsyncSession, pet_id: int):
    db_pet = await get_pet(db, pet_id)
    if db_pet:
        await db.delete(db_pet)
        await db.commit()
    return db_pet

async def get_pets_by_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(select(models.Pet).where(models.Pet.owner_id == owner_id))
    return result.scalars().all()