from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time



    
#===================================================================#
#==========  Schema:

class Post(BaseModel):
    title: str
    content: str
   #created_at: ? 

   

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
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_all_posts():
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    print(posts)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no posts in DB!"
        )
    return {"all_posts": posts}

# post detail by ID:
@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
async def get_post_by_id(id: int):
    cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    return {"post": post}


# create post:
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(front_post: Post):
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s,%s)",
                  (front_post.title, front_post.content)) 
    conn.commit()
    print("post created!")
    return {"created_post": front_post}


# delete a post:
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(id: int):
    cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *;", (id,))
    post_deleted = cursor.fetchone()
    print(post_deleted)
    if not post_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    conn.commit()
    return
    
# update a post:
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post_by_id(id: int, updated_post_data: Post):
    cursor.execute("UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *;", (updated_post_data.title, updated_post_data.content, id))
    post_up = cursor.fetchone()
    if not post_up:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with ID:{id} NOT FOUND!"
        )
    conn.commit()
    return {"updated_post": post_up}
 
