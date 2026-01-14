from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import UserLoginSchema
from app import models, oauth2
from app.utils import check_pw
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["authentication"]
)

# variable pour erreur de credentiales:
WRONG_CRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Wrong Credentials!"
)

@router.post("/login")
async def login(user_cred: OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise WRONG_CRED
    
    if not check_pw(user_cred.password, user.password):
        raise WRONG_CRED
    
    # create and return token
    token = oauth2.create_access_token({"user_id": user.id})

    return {"access_token":token,
            "token_type":"bearer"} 