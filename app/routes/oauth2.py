from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from .. import Schema
from ..config import setting
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()


    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credientials_exception):

    try:

        payload = jwt.decode(
            token,
            setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM],
        )

        id: int | None = payload.get("user_id")

        if id is None:
            raise credientials_exception
        token_data = Schema.TokenData(id = id)

    except (JWTError, ValidationError):
        raise credientials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
        credientials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return verify_access_token(token, credientials_exception)

    