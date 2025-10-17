from fastapi import APIRouter, Depends, HTTPException, status
from .. import models
from ..database import get_db
from ..schemas import user as user_schemas
from ..utils.hashing import Hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: user_schemas.UserLogin, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    if not Hash.verify_argon2(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    return {"detail": "Login successful"}