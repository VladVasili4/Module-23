from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
