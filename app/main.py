from fastapi import FastAPI, status
from app import models
from app.database import engine
from app.routers import posts, users, auth


# check si les tableaux existent , sinon les crees
models.Base.metadata.create_all(bind=engine)

# APP:
app = FastAPI()

# connect the routers:
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# test root
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Welcome to my API!"}



