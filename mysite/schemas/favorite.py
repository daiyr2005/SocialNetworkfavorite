
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FavoriteCreateSchema(BaseModel):
    post_id: int


class FavoriteItemResponseSchema(BaseModel):
    id: str

    favorite_id: str
    post_id: int

    post_title: Optional[str] = None
    post_description: Optional[str] = None

    created_date: datetime


class FavoriteResponseSchema(BaseModel):
    id: str

    user_id: int

    items: list[FavoriteItemResponseSchema] = []

    created_date: datetime
    update_date: datetime