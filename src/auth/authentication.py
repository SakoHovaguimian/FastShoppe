from fastapi import FastAPI, Depends, status, HTTPException
from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from src.custom_errors import MissingUserException
from src.database import get_db
from src import models
from src.hash import Hash
from . import oauth2

router = APIRouter(
    tags=["auth"]
)

@router.post('/token')
def get_token(
  request: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
):

    user =\
    (
        db
        .query(models.User)
        .filter(models.User.name == request.username)
        .first()
    )

    if not user:
        raise MissingUserException('User does not exist')
    
    if not Hash.verify(user.password, request.password):
        raise MissingUserException('Password is incorrect')

    access_token = oauth2.create_access_token(data={'sub' : user.name})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.name,
        'email': user.email
    }
