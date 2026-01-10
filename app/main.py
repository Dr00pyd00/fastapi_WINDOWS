from fastapi import FastAPI, status
from pydantic import BaseModel

# APP:
app = FastAPI()


# test root
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Welcome to my API!"}

    
#===================================================================#
#==========  Schema:

class POST(BaseModel):
    id: int
    title: str
    content: str
   #created_at: ? 

   
