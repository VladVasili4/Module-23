from fastapi import FastAPI, Depends, HTTPException, Form, Request, status, File, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app import models, crud, schemas, forms
from pydantic import BaseModel
from datetime import date, datetime, timedelta
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer



DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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


@app.get("/photos", response_class=HTMLResponse)
async def view_photos(request: Request, db: Session = Depends(get_db)):
    photos = crud.get_photos(db)
    # Временно передаем фиктивного пользователя
    current_user = {"id": 1, "username": "test_user"}
    return templates.TemplateResponse(
        "photos.html",
        {"request": request, "photos": photos, "current_user": current_user}
    )



# # @app.get("/photos", response_class=HTMLResponse)
# # async def view_photos(request: Request, db: Session = Depends(get_db)):
# #     photos = crud.get_photos(db)
# #     return templates.TemplateResponse("photos.html", {"request": request, "photos": photos})
#
#
# @app.get("/photos", response_class=HTMLResponse)
# async def view_photos(request: Request, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     photos = crud.get_photos(db)
#     return templates.TemplateResponse("photos.html", {"request": request, "photos": photos, "current_user": current_user})





@app.post("/photos")
async def upload_photo(
    db: Session = Depends(get_db),
    user_id: int = Form(...),
    file: UploadFile = File(...),
    description: str = Form(None)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    photo = schemas.PhotoCreate(filename=file.filename, description=description)
    return crud.add_photo(db, photo, user_id=user_id)

@app.post("/upload_photo")
async def upload_photo(file: UploadFile, db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    photo = models.Photo(filename=file.filename)  # Используем filename вместо path
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return {"photo_id": photo.id, "message": "Photo uploaded successfully"}


@app.post("/photos/{photo_id}/comments")
async def add_comment(
    photo_id: int,
    text: str = Form(...),  # Получаем текст комментария из формы
    user_id: int = Form(...),  # ID пользователя также передаётся через форму
    db: Session = Depends(get_db),
):
    comment_data = schemas.CommentCreate(text=text)
    comment = crud.add_comment(db, comment_data, user_id=user_id, photo_id=photo_id)
    return {"comment_id": comment.id, "message": "Comment added successfully"}







# @app.post("/photos/{photo_id}/comments")
# async def add_comment(
#     photo_id: int,
#     comment: schemas.CommentCreate,
#     db: Session = Depends(get_db),
#     user_id: int = Form(...)
# ):
#     return crud.add_comment(db, comment, user_id=user_id, photo_id=photo_id)

