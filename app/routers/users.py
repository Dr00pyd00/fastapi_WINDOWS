from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import UserCreateSchema, UserResponseSchema
from app import models
from typing import List
from app.utils import hash_pw, check_pw
from fastapi import status, HTTPException, Depends, APIRouter


# router:

router = APIRouter(
    prefix="/users",
    tags=['users']
)



#=================================================#
#================ USERS CRUD =====================#

# create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(user_new_cred: UserCreateSchema, db: Session = Depends(get_db) ):
    existing_user = db.query(models.User).filter(models.User.email == user_new_cred.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"email already taken!"
        )
    hashed_pw = hash_pw(user_new_cred.password)
    user_dict = user_new_cred.model_dump()
    user_dict["password"] = hashed_pw
    print(user_dict["password"])
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# retrieve user by id:
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def find_user_by_id(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} NOT FOUND!",
        )

    return user

