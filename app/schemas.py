from pydantic import BaseModel
from datetime import date
from typing import Optional
from typing import List

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


# Схемы для фотографий
class PhotoBase(BaseModel):
    filename: str
    description: Optional[str] = None

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    user_id: int
    comments: List["Comment"] = []

    class Config:
        orm_mode = True

# Схемы для комментариев
class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    photo_id: int
    user_id: int

    class Config:
        orm_mode = True
