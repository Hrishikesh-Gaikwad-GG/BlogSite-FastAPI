from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status, FastAPI
from sqlmodel import select

import schemas
from database import SessionDep
import models


import jwt
from jwt.exceptions import InvalidTokenError

from config import settings



SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes







pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = 'auto')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    

def get_user_with_email(email_id: str, session :  SessionDep):
    # return session.get(models.User, email_id)
    statement = select(models.User).where(models.User.email == email_id)
    item = session.exec(statement).first()
    return item

def authenticate_user(email_id: str, password, session : SessionDep):
    user = get_user_with_email(email_id , session)
    if not user:
        False
    if not verify_password(password, user.password):
        return False
    return user






def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = 15)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session : SessionDep):
    credentials_exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials, Please login again.",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exceptions
        token_data =  schemas.TokenData(email = email)
    except InvalidTokenError:
        raise credentials_exceptions
    user = get_user_with_email(token_data.email, session )
    if user is None:
        raise credentials_exceptions
    return user

    





router = APIRouter(
    tags= ["Token"]
)
# app = FastAPI()

@router.post("/token", response_model= schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session : SessionDep):

    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"}
            )
    
    access_token_expires = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.email}, expires_delta = access_token_expires
    )

    return {"access_token" : access_token, "token_type" : "bearer"}

@router.get("/debug/token")
async def debug_token(token: str = Depends(oauth2_scheme)):
    return {"your_token": token}


@router.get("/users/me", response_model = schemas.ResponseUser)
async def read_users_me(
    current_user: Annotated[schemas.ResponseUser, Depends(get_current_user)],
):
    return current_user

