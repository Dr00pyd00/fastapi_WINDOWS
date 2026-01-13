from pydantic import BaseModel, EmailStr
from datetime import datetime




#====================== POSTS =======================#

class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: bool = True



class PostCreateSchema(PostBaseSchema):
    pass


class PostUpdateSchema(PostBaseSchema):
    pass


# for th eresponse of db:
class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    # expliciter mode ORM V2:
    model_config = {"from_attributes":True}



#================ USERS ==============#

class UserBaseSchema(BaseModel):
    email: EmailStr

class UserCreateSchema(UserBaseSchema):
    password: str

class UserLoginSchema(UserBaseSchema):
    password: str 

class UserResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime

    model_config = {"from_attributes":True}

    