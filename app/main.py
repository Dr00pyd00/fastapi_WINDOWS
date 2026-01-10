from fastapi import FastAPI, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time



    
#===================================================================#
#==========  Schema:

class POST(BaseModel):
    id: int
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
    cursor.execute('SELECT * FROM posts;')
    posts = cursor.fetchall()
    print(posts)
    return {"all_posts": posts}