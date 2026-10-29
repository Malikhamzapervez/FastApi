from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import Schema, models, utils
from . import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])



@router.post("/login", response_model = Schema.Token)
def login(user_credientials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credientials.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Invalid Credientials")

    
    if not utils.verify(user_credientials.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="Invalid Credientials")

    #create a token and return the token 

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token" : access_token, "token_type":"bearer"}