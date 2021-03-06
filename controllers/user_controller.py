from os import error
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from fastapi.param_functions import Query
from sqlalchemy.sql.functions import mode, user
from typing import List, Optional
import schemas, models
from custom_errors import MissingItemException
from database import get_db
from sqlalchemy.orm import Session
from hash import Hash

router = APIRouter(
    prefix='/users',
    tags=["users"]   
)

#! GET ALL USERS
@router.get(
    "/",
    status_code=200,
    response_model=List[schemas.UserResponse]
)
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users

#! GET USER
@router.get(
    '/{user_id}',
    status_code=200,
    response_model=schemas.UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    
    user =\
    (
        db
        .query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if not user: 

        errorString = f"id {user} does not exist"
        raise MissingItemException(errorString)

    return user

#! CREATE USER
@router.post(
    "/",
    status_code=200,
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreateResponse,
    db: Session = Depends(get_db)
):
    
    newUser = models.User(
        name = user.name,
        email = user.email,
        password= Hash.bcrypt(user.password)
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return newUser

def get_user_by_username(db: Session, name: str):

  user = db.query(models.User).filter(models.User.name == name).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {name} not found')

  return user