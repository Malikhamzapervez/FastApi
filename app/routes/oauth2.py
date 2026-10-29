from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import Schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#secret Key
#Algorithms
#Expression time

SECRET_KEY = "DKFDJBNDVDVDNVJDNKSNKSNDKSNFE97R3899R0376GBWNRNBFCIY8W9EUW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict):
    to_encode = data.copy()


    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credientials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credientials_exception
        token_data = Schema.TokenData(id = id)

    except JWTError:
            raise credientials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
        credientials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credientials", headers = {"www-Authenticate":"Bearer"})
        return verify_access_token(token, credientials_exception)

    