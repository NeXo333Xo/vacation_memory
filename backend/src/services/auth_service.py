from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from sqlmodel import Session

from backend.src.crud.users_crud import create_user, get_user_by_email, get_user_by_username
from backend.src.models.models import Token, TokenData, UserCreate, UserInDB, UserRead
from backend.src.services.security import verify_password, oauth2_scheme
from backend.src.utils import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY



def register_user(db: Session, user_data: UserCreate) -> UserRead:
    """Registriert einen neuen Benutzer"""
    user = get_user_by_username(db, user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username existiert bereits")
    
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email existiert bereits")
    
    
    new_user = create_user(db, user_data)
    return new_user


def login_user(db: Session, form_data: OAuth2PasswordRequestForm) -> Token:
    """Authentifiziert den Benutzer und gibt ein JWT-Token zurück."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falscher Benutzername oder Passwort",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


def authenticate_user(db: Session, username: str, password: str) -> UserInDB | bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[UserRead, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


