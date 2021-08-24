import os
from typing import List, Optional
from passlib.context import CryptContext
from fastapi import (
    BackgroundTasks,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
    status,
)
from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
)
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from app.models import User
import jwt
from app.templates import templates
from pathlib import Path
import cloudinary
import cloudinary.uploader

config_credentials = dotenv_values(".env")
################################################################
############################ EMAIL #############################
################################################################
conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["EMAIL"],
    MAIL_PASSWORD=config_credentials["PASS"],
    MAIL_FROM=config_credentials["EMAIL"],
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)


class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str


async def send_mail(email: EmailSchema):
    message = MessageSchema(
        subject=email.dict().get("subject"),
        email=email.dict().get("email"),
        body=email.dict.get("body"),
    )
    fm = FastMail(conf)
    fm.send_message(message)


################################################################
######################   AUTHENTICATION  #######################
################################################################
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def generate_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        plain_password, hashed_password
    )


async def authenticate_user(username: str, password: str):
    user = await User.get_or_none(username=username)
    if user and verify_password(password, user.password):
        return user
    return False


async def token_generator(username: str, password: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Username or Password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await authenticate_user(username, password)
    print(user)
    if not user:
        raise credentials_exception

    token_data = {"username": user.username, "id": user.id}
    token = jwt.encode(
        token_data, config_credentials["SECRET"]
    )
    return token


################################################################
############################  APP  #############################
################################################################


async def save_file(file: UploadFile = File(...)):
    filename = file.filename
    extension = filename.split(".")[1]
    if extension.lower() not in [
        "tif",
        "tiff",
        "jpg",
        "jpeg",
        "png",
        "webp",
        "jfif",
    ]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="This image type isn't allowed",
        )
    result = cloudinary.uploader.upload(
        file.file, folder="ApRestaurant", secure=True
    )
    url = result.get("url")
    return url
