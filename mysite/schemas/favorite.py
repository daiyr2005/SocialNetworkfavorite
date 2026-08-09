
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FavoriteResponseSchema(BaseModel):
    id: str
    user_id: int
    created_date: datetime

class FavoriteItemCreateSchema(BaseModel):
    favorite: int
    favorite_name: str = Field(min_length=1, max_length=50)
    content: str


class FavoriteItemUpdateSchema(BaseModel):
    favorite_name: str = Field(min_length=1, max_length=50)
    content: str

class FavoriteItemResponseSchema(BaseModel):
    id: str
    favorite: int
    favorite_name: str
    content: str
    created_date: datetime
    updated_date: datetime

class FavoriteCreateSchema(BaseModel):
    post_id: int



