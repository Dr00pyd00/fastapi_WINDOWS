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

