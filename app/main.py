from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.schemas import PostCreateSchema, PostUpdateSchema, PostResponseSchema, UserCreateSchema, UserResponseSchema
import app.models
from typing import List
from app.utils import hash_pw, check_pw


  # check si les tableaux existent , sinon les crees
models.Base.metadata.create_all(bind=engine)



# Access to DB:
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tutoDB",
            user="postgres",
            password="kottak",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DATABSE CONNECTED!")
        break
    except Exception as e:
        print(f"ERROR CONNECTION DB: {e}")
        time.sleep(2)

        
# APP:
app = FastAPI()


# test root
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Welcome to my API!"}



#====================================================================#
#================= CRUD ================================#

# all posts:
@app.get("/posts", status_code=status.HTTP_200_OK, response_model=List[PostResponseSchema])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no posts in DB!"
        )
    return posts

# post detail by ID:
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    return post 


# create post:
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(front_post: PostCreateSchema, db: Session = Depends(get_db)):
    print(front_post.model_dump())
    new_post = models.Post(**front_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    print("post created!")
    return new_post 

# delete a post:
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int, db: Session = Depends(get_db) ):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    db.delete(post_to_delete)
    db.commit()
    return
    
# update a post:
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def update_post_by_id(id: int, updated_post_data: PostUpdateSchema, db: Session = Depends(get_db)):
    post_to_up = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_to_up:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    for k,v in updated_post_data.model_dump().items():
        setattr(post_to_up, k, v)
    db.commit()
    db.refresh(post_to_up)
    
    return post_to_up 




#=================================================#
#================ USERS CRUD =====================#

# create user
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
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
@app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def find_user_by_id(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} NOT FOUND!",
        )

    return user

