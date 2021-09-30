from os import error
from fastapi import FastAPI, Depends, status, Response, HTTPException, APIRouter
from fastapi.param_functions import Query
from sqlalchemy.sql.functions import mode, user
from typing import List, Optional
from src import schemas, models
from src.custom_errors import MissingItemException
from src.database import get_db
from sqlalchemy.orm import Session
from src.auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/items',
    tags=["items"]   
)

## Get Items
@router.get(
    "/",
    status_code=200,
    response_model=List[schemas.ItemResponse],
    summary= "This gets all the items in the database",
    description="Get all the items in the database"
)
def get_items(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    
    items = db.query(models.Item).all()
    return items

## Get an Item
@router.get(
    "/{item_id}",
    status_code=200,
    response_model=schemas.ItemResponse
)
def get_item(
    item_id: int,
    fakeRequirement: int = Query(
        None,
        title="This is just to see if the docs generate",
        description="Did this work?",
        depricated=False,
        gt=1
    ),
    fakeString: str = Query(
    None,
    title="String Test",
    description="Fasle Character length checker",
    depricated=True,
    min_length=3
    ),
    db: Session = Depends(get_db)
):
    
    item =\
    (
        db
        .query(models.Item)
        .filter(models.Item.id == item_id)
        .first()
    )

    if not item: 
        # raise HTTPException(
        #     status.HTTP_404_NOT_FOUND,
        #     detail=f"item with id: {item_id} was not found."
        # )

        errorString = f"id {item_id} does not exist"
        raise MissingItemException(errorString)

    return item

## Get Items by Tag
@router.get(
    "/tag/{tag_id}",
    status_code=200,
    response_model=List[schemas.ItemResponse]
)
def get_items(tag_id: int, db: Session = Depends(get_db)):
    
    items =\
    (
        db
        .query(models.Item)
        .filter(models.Item.tag_id == tag_id)
        .all()
    )

    return items

## Get Items by Status
@router.get(
    "/status/{status}",
    status_code=200,
    response_model=List[schemas.ItemResponse]
)
def get_items(status: int, db: Session = Depends(get_db)):
    
    items =\
    (
        db
        .query(models.Item)
        .filter(models.Item.status == status)
        .all()
    )

    return items

## Create Item
@router.post(
    "/",
    status_code=201,
    response_model=schemas.ItemCreateResponse
)
def create_item(item: schemas.ItemCreateResponse, db: Session = Depends(get_db)):

    new_item = models.Item(
        title = item.title,
        description = item.description,
        price = item.price,
        status = item.status,
        user_id = item.user_id,
        tag_id = item.tag_id
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
    
## Update Item
@router.put(
    "/{item_id}",
    status_code=202,
    response_model=schemas.ItemResponse
)
def update_item(
    item_id: int,
    item: schemas.ItemUpdateResponse,
    db: Session = Depends(get_db)
 ):
    
    originalItem =\
    (
        db
        .query(models.Item)
        .filter(models.Item.id == item_id)
    )

    if not originalItem.first():
        raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail = f"Item with the id: {id} was not found."
    )

    originalItem.update(
    {
        "title": item.title,
        "description": item.description,
        "status" : item.status,
        "price": item.price 
    })
    db.commit()

    item = get_item(item_id, db)
    return item

