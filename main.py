from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from random import randrange




app = FastAPI()

class social_media_app(BaseModel):
    title : Annotated[str, Field(description='Title is must')]
    content : Optional[str] = None
    published : bool = True
    rating : Annotated[int, Field(gt =0,lt=5, description="This is Optional field and rate between 1-5")] = Field(default=None)
    

my_post_data =[ { 'title':"Title of post 1", "content":"Content of post 1", "id":1}, { 'title':"Favourite Foods", "content":"Pizza, burger", "id":2}, { 'title':"Title of post 3", "content":"Content of post 3", "id": None}]
def find_post(id):
    for i in my_post_data:
        if i["id"]==id:
            return i
@app.get('/')
def first():
    return {'message': 'First! Endpoint hit'}

@app.get('/Posts')
def posts():
    return {'message': my_post_data}

@app.post('/Posts')
def create_post(Post: social_media_app):
    post_dict = Post.dict()
    post_dict['id']= randrange(0,10000000)

    my_post_data.append(post_dict)
    return {'message':my_post_data}


@app.get("/Post/{id}")
def get_post(id:int):
    x = find_post(id)

    return {"Pop-up" : f"Here is the post{x}"}
