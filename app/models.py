from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CustomUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'



# Фото пользователя
class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user = relationship("CustomUser", back_populates="photos")

# Комментарии к фото
class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey('photos.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text, nullable=False)
    user = relationship("CustomUser", back_populates="comments")
    photo = relationship("Photo", back_populates="comments")

# Обновление существующих моделей
CustomUser.photos = relationship("Photo", back_populates="user")
CustomUser.comments = relationship("Comment", back_populates="user")
Photo.comments = relationship("Comment", back_populates="photo")
