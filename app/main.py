from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db, Base


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class social_media_app(BaseModel):
    title : Annotated[str, Field(description='Title is must')]
    content : Optional[str] = None
    published : bool = True
    #rating : Annotated[int, Field(gt =0,lt=5, description="This is Optional field and rate between 1-5")] = Field(default=None)


while True:   
    try:
        conn = psycopg2.connect(host="localhost", database="social_media_app",user="postgres",password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was sucessfull")
        break
    except Exception as error:
        print("Connecting to Database failed....")
        print("Error :", error)
        time.sleep(2)

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
def posts(db: Session = Depends(get_db)):
    Postss = db.query(models.Post).all()
   # cursor.execute("""SELECT * FROM "Posts" """)
   # posts = cursor.fetchall()

    
    return {'message': Postss}

@app.post('/Posts', status_code=201) # Changing the default status code from 200 OK to 201 CREATED
def create_post(Post: social_media_app, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (Post.title, Post.content, Post.published))
    #new_post = cursor.fetchone()
    #conn.commit() 
    #new_post = models.Post(title=Post.title, content= Post.content, published = Post.published)
    new_post = models.Post(**Post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'message': new_post}


@app.get("/Posts/sqlalchemy")
def get_posts_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'Data': posts}


@app.get("/Posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
   # cursor.execute("""SELECT * FROM "Posts" WHERE id = %s""", (id,))
   # post = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id).first()

  

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return {"data": posts}



@app.delete("/Post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  #  cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (id,))
  #  deleted = cursor.fetchone()
  #  conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/Posts/{id}")
def update_post(id: int, posts: social_media_app, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    updated_post.update(posts.dict(), synchronize_session = False)
    db.commit()
    return {"data": updated_post.first()}


