from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.param_functions import Query
from sqlalchemy.sql.functions import mode, user
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
# from .hashing import Hash
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

## Get Items
@app.get(
    "/items",
    tags=["Item"],
    status_code=200,
    response_model=List[schemas.ItemResponse]
)
def get_items(db: Session = Depends(get_db)):
    
    items = db.query(models.Item).all()
    return items

## Get an Item
@app.get(
    "/items/{item_id}",
    tags=["Item"],
    status_code=200,
    response_model=schemas.ItemResponse
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    
    item =\
    (
        db
        .query(models.Item)
        .filter(models.Item.id == item_id)
        .first()
    )

    if not item: 
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"item with id: {item_id} was not found."
        )

    return item

## Get Items by Tag
@app.get(
    "/items/tag/{tag_id}",
    tags=["Item"],
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
@app.get(
    "/items/status/{status}",
    tags=["Item"],
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
@app.post(
    "/items",
    tags=["Item"],
    status_code=201,
    response_model=schemas.ItemCreateResponse
)
def create_item(item: schemas.ItemCreateResponse, db: Session = Depends(get_db)):
    
    print(item.status)

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
@app.put(
    "/items/{item_id}",
    tags=["Item"],
    status_code=202,
    response_model=schemas.ItemResponse
)
def update_item(item_id: int, item: schemas.ItemUpdateResponse, db: Session = Depends(get_db)):
    
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