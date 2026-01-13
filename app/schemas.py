from pydantic import BaseModel
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
    email: str
    password: str

class UserCreateSchema(UserBaseSchema):
    pass

class UserLoginSchema(UserBaseSchema):
    pass 

class UserResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime