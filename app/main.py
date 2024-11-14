from fastapi import FastAPI, Depends, HTTPException, Form, Request, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app import models, crud, schemas, forms
from pydantic import BaseModel
from datetime import date

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


# Получение текущей сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Регистрация нового пользователя
@app.get("/reg", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/reg")
async def register_user(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_data = forms.UserRegistrationForm(
        username=form_data.get("username"),
        first_name=form_data.get("first_name"),
        last_name=form_data.get("last_name"),
        email=form_data.get("email"),
        phone_number=form_data.get("phone_number"),
        birth_date=form_data.get("birth_date"),
        password=form_data.get("password"),
        confirm_password=form_data.get("confirm_password"),
    )

    user_data.check_passwords()

    user = schemas.UserCreate(**user_data.dict())
    crud.create_user(db, user)
    return {"message": "User registered successfully"}


# Список пользователей
@app.get("/list", response_class=HTMLResponse)
async def users_list(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

