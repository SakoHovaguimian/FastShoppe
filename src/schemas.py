from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.sql.sqltypes import Float

class UserResponse(BaseModel):
    
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

class Tag(BaseModel):
    
    id: int
    title: str

    class Config:
        orm_mode = True

class ItemCreateResponse(BaseModel):

    title: str
    description: str
    price: float
    status: int
    user_id: int
    tag_id: int

    class Config:
        orm_mode = True

class ItemUpdateResponse(BaseModel):
    
    title: str
    description: str
    price: float
    status: int

    class Config:
        orm_mode = True

class ItemResponse(BaseModel):

    id: int
    title: str
    description: str
    price: float
    status: int

    tag: Tag
    user: UserResponse

    class Config:
        orm_mode = True