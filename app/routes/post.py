
from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from typing import List
from sqlalchemy.orm import Session
from .. import models, Schema
from ..database import get_db
from . import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])



#@router.get("", response_model=List[Schema.Post])
@router.get("", response_model=List[Schema.PostOut])
def posts(
    db: Session = Depends(get_db),
    user_id: Schema.TokenData = Depends(oauth2.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    search: str = "",
):
    post_query = (
        db.query(models.Post)
        .filter(models.Post.owner_id == user_id.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip).all()
    )
   # cursor.execute("""SELECT * FROM "Posts" """)
   # posts = cursor.fetchall()

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True). group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    )
    return results

@router.post("", status_code=201, response_model=Schema.Post)
def create_post(post: Schema.PostCreate, db: Session = Depends(get_db), user_id: Schema.TokenData = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (Post.title, Post.content, Post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=Post.title, content= Post.content, published = Post.published)
    new_post = models.Post(**post.model_dump(), owner_id=user_id.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post



@router.get('/{id}', response_model=Schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id: Schema.TokenData = Depends(oauth2.get_current_user)):
   # cursor.execute("""SELECT * FROM "Posts" WHERE id = %s""", (id,))
   # post = cursor.fetchone()
    #posts = db.query(models.Post).filter(models.Post.id == id).first()

    post_result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True). group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    post, _ = post_result
    if post.owner_id != user_id.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perfor, request action')

    return post_result



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: Schema.TokenData = Depends(oauth2.get_current_user)):
  #  cursor.execute("""DELETE FROM "Posts" WHERE id = %s RETURNING *""", (id,))
  #  deleted = cursor.fetchone()
  #  conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    if post.owner_id != user_id.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perfor, request action')
    post_query.delete(synchronize_session = False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Schema.Post)
def update_post(id: int, posts: Schema.PostCreate, db: Session = Depends(get_db), user_id: Schema.TokenData = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE "Posts" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #               (post.title, post.content, post.published, id))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:  # updated_post.first() grabs the top entry
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")

    if post.owner_id != user_id.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'Not authorized to perfor, request action')

    for field, value in posts.model_dump().items():
        setattr(post, field, value)

    db.commit() #to save the changes we use commit
    db.refresh(post)

    return post
