from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional,Annotated
from datetime import datetime




class PostBase(BaseModel):
    title : Annotated[str, Field(description='Title is must')]
    content : Optional[str] = None
    published : bool = True
    #rating : Annotated[int, Field(gt =0,lt=5, description="This is Optional field and rate between 1-5")] = Field(default=None)


class PostCreate(PostBase):
    pass


class Post(PostBase):
#    title : str              <<<All the three fields are inherited>>>>>
#   content : str             <<<if i want to add new field which is specific to one method than i will define it here like e.g,>>
#   published : bool = True

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=1, max_length=72)]


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
