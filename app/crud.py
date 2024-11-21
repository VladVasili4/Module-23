from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.CustomUser(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        birth_date=user.birth_date,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CustomUser).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.CustomUser).filter(models.CustomUser.username == username).first()

# Добавить фото
def add_photo(db: Session, photo: schemas.PhotoCreate, user_id: int):
    db_photo = models.Photo(**photo.dict(), user_id=user_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

# Получить все фото
def get_photos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Photo).offset(skip).limit(limit).all()

# Добавить комментарий
def add_comment(db: Session, comment: schemas.CommentCreate, user_id: int, photo_id: int):
    db_comment = models.Comment(**comment.dict(), user_id=user_id, photo_id=photo_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Получить комментарии к фото
def get_comments_by_photo(db: Session, photo_id: int):
    return db.query(models.Comment).filter(models.Comment.photo_id == photo_id).all()
