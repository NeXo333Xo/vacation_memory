from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.database.database import SessionDep
from backend.src.models.models import Token, UserCreate, UserRead
from backend.src.services.auth_service import login_user, register_user


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=201)
async def register_user_route(db: SessionDep, user_data: UserCreate):
    return register_user(db, user_data)


@router.post("/login", response_model=Token, status_code=201)
async def login_for_access_token(
    db: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    return login_user(db, form_data)


    


