from fastapi import FastAPI, Response, status, HTTPException
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

def find_index(id):
    for i,p in enumerate(my_post_data):
        if p['id']==id:
            return i
        
@app.get('/')
def first():
    return {'message': 'First! Endpoint hit'}

@app.get('/Posts')
def posts():
    return {'message': my_post_data}

@app.post('/Posts', status_code=201) # Changing the default status code from 200 OK to 201 CREATED
def create_post(Post: social_media_app):
    post_dict = Post.dict()
    post_dict['id']= randrange(0,10000000)

    my_post_data.append(post_dict)
    return {'message':my_post_data}


@app.get("/Posts/{id}")
def get_post(id:int, response:Response):
    x = find_post(id)
    if not x:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found") # if post not exist 
   #     response.status_code=status.HTTP_404_NOT_FOUND
   #     return {"Error" : f"Post with id {x} was not found"}
        

    return {"Pop-up" : f"Here is the post{x}"}



@app.delete("/Post/{id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index  = find_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    my_post_data.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/Posts/{id}")
def update_post(id:int, post:social_media_app):

    index  = find_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict['id']=id
    my_post_data[index] = post_dict
    return {"data":post_dict}


