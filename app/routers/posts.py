
from app.database import get_db
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import PostCreateSchema, PostUpdateSchema, PostResponseSchema
from typing import List
from app import models

# router:
router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#====================================================================#
#================= CRUD ================================#

# all posts:
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponseSchema])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no posts in DB!"
        )
    return posts

# post detail by ID:
@router.get("//{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    return post 


# create post:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
async def create_post(front_post: PostCreateSchema, db: Session = Depends(get_db)):
    print(front_post.model_dump())
    new_post = models.Post(**front_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    print("post created!")
    return new_post 

# delete a post:
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
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

