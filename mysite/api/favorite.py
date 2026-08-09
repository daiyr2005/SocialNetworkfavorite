from datetime import datetime, timezone
from typing import Annotated, List

from bson import ObjectId

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from mysite.schemas.favorite import (
    FavoriteItemCreateSchema,
    FavoriteItemUpdateSchema,
    FavoriteItemResponseSchema,
    FavoriteResponseSchema
)

from mysite.database.mongodb import (
    get_favorite_connection,
    get_favorite_item_connection
)

from mysite.database.mapper import (
    favorite_document_to_response,
    favorite_items_document_to_response
)

from .dependencies import get_current_user


favorite_router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"]
)


# =========================
# FAVORITE
# =========================

@favorite_router.get(
    "/",
    response_model=List[FavoriteResponseSchema]
)
async def favorite_list(
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    collection = get_favorite_connection()

    cursor = collection.find({
        "user_id": current_user["id"]
    })

    favorites = []

    async for favorite in cursor:
        favorites.append(
            favorite_document_to_response(
                favorite
            )
        )

    return favorites


@favorite_router.post(
    "/",
    response_model=FavoriteResponseSchema
)
async def add_favorite(
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    collection = get_favorite_connection()

    favorite_document = {
        "user_id": current_user["id"],
        "created_date": datetime.now(timezone.utc)
    }

    result = await collection.insert_one(
        favorite_document
    )

    favorite_document["_id"] = result.inserted_id

    return favorite_document_to_response(
        favorite_document
    )


# =========================
# FAVORITE ITEM
# =========================

@favorite_router.post(
    "/items/",
    response_model=FavoriteItemResponseSchema
)
async def add_favorite_item(
    favorite: FavoriteItemCreateSchema,
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    favorite_collection = get_favorite_connection()

    favorite_document = await favorite_collection.find_one({
        "user_id": current_user["id"]
    })

    if not favorite_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )

    item_collection = get_favorite_item_connection()

    item_document = {
        "favorite": favorite.favorite,
        "favorite_name": favorite.favorite_name,
        "content": favorite.content,
        "created_date": datetime.now(timezone.utc),
        "updated_date": datetime.now(timezone.utc)
    }

    result = await item_collection.insert_one(
        item_document
    )

    item_document["_id"] = result.inserted_id

    return favorite_items_document_to_response(
        item_document
    )


@favorite_router.put(
    "/items/{item_id}",
    response_model=FavoriteItemResponseSchema
)
async def update_favorite_item(
    item_id: str,
    favorite: FavoriteItemUpdateSchema,
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    item_collection = get_favorite_item_connection()

    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item id"
        )

    item_document = await item_collection.find_one({
        "_id": object_id
    })

    if not item_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite item not found"
        )

    result = await item_collection.update_one(
        {
            "_id": object_id
        },
        {
            "$set": {
                "favorite_name": favorite.favorite_name,
                "content": favorite.content,
                "updated_date": datetime.now(timezone.utc)
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Favorite item was not updated"
        )

    updated_document = await item_collection.find_one({
        "_id": object_id
    })

    return favorite_items_document_to_response(
        updated_document
    )


@favorite_router.delete(
    "/items/{item_id}"
)
async def delete_favorite_item(
    item_id: str,
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    item_collection = get_favorite_item_connection()

    try:
        object_id = ObjectId(item_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item id"
        )

    result = await item_collection.delete_one({
        "_id": object_id
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite item not found"
        )

    return {
        "detail": "Favorite item deleted"
    }