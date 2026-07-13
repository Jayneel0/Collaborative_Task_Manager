from pwdlib import PasswordHash
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from fastapi.security import OAuth2PasswordBearer

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password : str, hashed_password : str):
    return password_hash.verify(password, hashed_password)

SECRET_KEY = "Change_this_to_a_random_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/users/login")

def get_current_user(token : str = Depends(oauth2_scheme), db : Session=Depends(get_db)):
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    user = crud.get_user(db, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user