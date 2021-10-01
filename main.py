from fastapi import FastAPI, Depends, status, Response, HTTPException, Request
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse
from sqlalchemy.sql.functions import mode, user
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

from typing import List
from controllers import item_controller, user_controller
from custom_errors import MissingItemException, MissingUserException
from auth import authentication

app = FastAPI()

app.include_router(authentication.router)
app.include_router(item_controller.router)
app.include_router(user_controller.router)

models.Base.metadata.create_all(engine)

#Handle Errors
@app.exception_handler(MissingItemException)
def missing_item_expeption_handler(request: Request, exc: MissingItemException):

    statusCode = status.HTTP_404_NOT_FOUND

    return JSONResponse(

        status_code=statusCode,
        content={
            'error': {
                'message': exc.message,
                'status_code': statusCode
            }
        }
 )

@app.exception_handler(MissingUserException)
def missing_user_expeption_handler(request: Request, exc: MissingUserException):

    statusCode = status.HTTP_404_NOT_FOUND

    return JSONResponse(

        status_code=statusCode,
        content={
            'error': {
                'message': exc.message,
                'status_code': statusCode
            }
        }
 )