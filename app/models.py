from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

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
