from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
import jwt
from dotenv import dotenv_values
from app.models import User

config_credentials = dotenv_values(".env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token Passed",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            config_credentials["SECRET"],
            algorithms=["HS256"],
        )
        user = await User.get(id=payload.get("id"))
        return user
    except:
        raise credentials_exception

    # return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


async def get_admin_user(
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not admin user",
        )

    return current_user
