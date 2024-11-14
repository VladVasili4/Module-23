from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserRegistrationForm(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    password: str
    confirm_password: str

    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
