from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.security import (verify_password,
                          create_access_token,
                          get_current_user,
                          blacklisted_tokens,
                          oauth2_scheme)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users")

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db : Session = Depends(get_db)):
    return crud.get_users(db)
    
@router.post("/", response_model=schemas.UserResponse)
def create_user(user : schemas.UserCreate,
                db : Session= Depends(get_db)):
    return crud.create_user(db, user)

@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id : int,
                update : schemas.UserUpdate,
                current_user : models.User = Depends(get_current_user),
                db : Session=Depends(get_db)):
    if (user_id != current_user.id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to update this user"
        )
    return crud.update_user(db, user_id, update)

@router.delete("/{user_id}")
def delete_user(user_id : int,
                current_user : models.User = Depends(get_current_user),
                db : Session = Depends(get_db)):
    if (user_id != current_user.id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this user"
        )
    crud.delete_user(db, user_id)
    return {
        "message" : "User Deleted Succesfully"
    }

@router.post("/login", response_model=schemas.Token)
def login(form_data : OAuth2PasswordRequestForm=Depends(),
          db : Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if user is None :
        raise HTTPException(
            status_code=401,
            detail = "User email or password invalid"
        )
    elif not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail = "User email or password invalid"
        )
    access_token = create_access_token(
        {
            "sub" : str(user.id)
        }
    )
    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }
    
@router.post("/logout")
def logout(current_user: models.User = Depends(get_current_user),
           token: str = Depends(oauth2_scheme),):
    blacklisted_tokens.add(token)
    return {
        "message": "Logged out successfully"
    }

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user : models.User=Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id : int, db : Session = Depends(get_db)):
    return crud.get_user(db, user_id)

