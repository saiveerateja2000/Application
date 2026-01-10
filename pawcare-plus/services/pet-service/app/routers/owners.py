from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/owners/", response_model=schemas.Owner)
async def create_owner(owner: schemas.OwnerCreate, db: AsyncSession = Depends(get_db)):
    db_owner = await crud.create_owner(db=db, owner=owner)
    return db_owner

@router.get("/owners/", response_model=List[schemas.Owner])
async def read_owners(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    owners = await crud.get_owners(db, skip=skip, limit=limit)
    return owners

@router.get("/owners/{owner_id}", response_model=schemas.Owner)
async def read_owner(owner_id: int, db: AsyncSession = Depends(get_db)):
    db_owner = await crud.get_owner(db, owner_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db_owner

@router.put("/owners/{owner_id}", response_model=schemas.Owner)
async def update_owner(owner_id: int, owner: schemas.OwnerCreate, db: AsyncSession = Depends(get_db)):
    db_owner = await crud.update_owner(db, owner_id=owner_id, owner=owner)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db_owner

@router.delete("/owners/{owner_id}")
async def delete_owner(owner_id: int, db: AsyncSession = Depends(get_db)):
    db_owner = await crud.delete_owner(db, owner_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return {"message": "Owner deleted"}