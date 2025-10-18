from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from .. import models
from ..database import get_db
from ..schemas import user as user_schemas, token as token_schemas
from ..utils.hashing import Hash
from ..utils.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=token_schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not Hash.verify_argon2(request.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}