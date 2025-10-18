from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models
from app.database import get_db
from ..schemas import token as token_schemas
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from ..config import settings

SECRET_KEY = settings.SECRET_KEY
TOKEN_ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception) -> token_schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        id: str = payload.get("user_id")
        email: str = payload.get("email")
        if id is None:
            raise credentials_exception
        token_data = token_schemas.TokenData(id=id, email=email)
        return token_data
    except InvalidTokenError:
        raise credentials_exception
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user