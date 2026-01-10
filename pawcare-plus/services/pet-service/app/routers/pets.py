from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/pets/", response_model=schemas.Pet)
async def create_pet(pet: schemas.PetCreate, db: AsyncSession = Depends(get_db)):
    # Check if owner exists
    owner = await crud.get_owner(db, pet.owner_id)
    if not owner:
        raise HTTPException(status_code=400, detail="Owner not found")
    db_pet = await crud.create_pet(db=db, pet=pet)
    return db_pet

@router.get("/pets/", response_model=List[schemas.Pet])
async def read_pets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    pets = await crud.get_pets(db, skip=skip, limit=limit)
    return pets

@router.get("/pets/{pet_id}", response_model=schemas.Pet)
async def read_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    db_pet = await crud.get_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

@router.put("/pets/{pet_id}", response_model=schemas.Pet)
async def update_pet(pet_id: int, pet: schemas.PetCreate, db: AsyncSession = Depends(get_db)):
    # Check if owner exists
    owner = await crud.get_owner(db, pet.owner_id)
    if not owner:
        raise HTTPException(status_code=400, detail="Owner not found")
    db_pet = await crud.update_pet(db, pet_id=pet_id, pet=pet)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    db_pet = await crud.delete_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return {"message": "Pet deleted"}

@router.get("/owners/{owner_id}/pets", response_model=List[schemas.Pet])
async def read_pets_by_owner(owner_id: int, db: AsyncSession = Depends(get_db)):
    owner = await crud.get_owner(db, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    pets = await crud.get_pets_by_owner(db, owner_id=owner_id)
    return pets