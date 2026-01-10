from pydantic import BaseModel
from typing import Optional

class OwnerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class OwnerCreate(OwnerBase):
    pass

class Owner(OwnerBase):
    id: int

    class Config:
        from_attributes = True

class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    age: Optional[int] = None
    owner_id: int

class PetCreate(PetBase):
    pass

class Pet(PetBase):
    id: int

    class Config:
        from_attributes = True

class PetWithOwner(Pet):
    owner: Owner