from datetime import datetime, timezone
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from mysite.schemas.favorite import (
    FavoriteCreateSchema,
    FavoriteResponseSchema
)

from mysite.database.mongodb import get_favorite_connection
from mysite.database.mapper import favorite_document_to_response

from mysite.clients.post_service import get_post

from .dependencies import get_current_user


favorite_router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)



@favorite_router.get(
    "/",
    response_model=List[FavoriteResponseSchema]
)
async def favorite_list(
    current_user: Annotated[dict, Depends(get_current_user)]
):

    collection = await get_favorite_connection()


    cursor = collection.find(
        {
            "user_id": current_user["id"]
        }
    )


    favorites = []

    async for favorite in cursor:

        favorites.append(
            favorite_document_to_response(favorite)
        )


    return favorites



@favorite_router.post(
    "/",
    response_model=FavoriteResponseSchema
)
async def add_favorite(
    favorite: FavoriteCreateSchema,
    current_user: Annotated[dict, Depends(get_current_user)]
):

    post = await get_post(
        favorite.post_id
    )


    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )


    collection = await get_favorite_connection()


    favorite_document = {

        "user_id": current_user["id"],

        "items": [
            {
                "post_id": favorite.post_id,

                "post_title": post.get("title"),

                "post_description": post.get("description"),

                "created_date": datetime.now(timezone.utc)
            }
        ],

        "created_date": datetime.now(timezone.utc),

        "update_date": datetime.now(timezone.utc)
    }


    result = await collection.insert_one(
        favorite_document
    )


    favorite_document["_id"] = result.inserted_id


    return favorite_document_to_response(
        favorite_document
    )