from pydantic import BaseModel




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
class PostResponseSchema(BaseModel):
    title: str
    content: str
    published: bool