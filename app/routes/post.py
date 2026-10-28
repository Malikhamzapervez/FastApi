
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, Schema
from ..database import get_db

router = APIRouter(prefix="/Posts")



@router.get("" , response_model=List[Schema.Post])
def posts(db: Session = Depends(get_db)):
    Retrieved_Post = db.query(models.Post).all()
   # cursor.execute("""SELECT * FROM "Posts" """)
   # posts = cursor.fetchall()

    
    return Retrieved_Post

@router.post('', status_code=201, response_model=Schema.Post)
def create_post(post: Schema.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (Post.title, Post.content, Post.published))
    #new_post = cursor.fetchone()
    #conn.commit() 
    #new_post = models.Post(title=Post.title, content= Post.content, published = Post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post



@router.get('/{id}', response_model=Schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
   # cursor.execute("""SELECT * FROM "Posts" WHERE id = %s""", (id,))
   # post = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id).first()

  

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    return posts



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  #  cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (id,))
  #  deleted = cursor.fetchone()
  #  conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Schema.Post)
def update_post(id: int, posts: Schema.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None: #updated_post.first() grabs the top entry 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    updated_post.update(posts.model_dump(), synchronize_session=False)
    db.commit() #to save the changes we use commit
    return updated_post.first()
