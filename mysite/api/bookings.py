import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List

from mysite.schemas.order import OrderResponseSchema, OrderCreateSchema, OrderStatus
from mysite.database.mongodb import get_order_connection
from mysite.database.mapper import glovo_document_to_response
from mysite.clients.store_service import get_store, get_product

from .dependencies import get_current_user


order_router = APIRouter(prefix="/order", tags=["Glovo"])


@order_router.get("/", response_model=List[OrderResponseSchema])
async def order_list(current_user: Annotated[dict, Depends(get_current_user)]):
    collection = await get_order_connection()

    cursor = collection.find(
        {"user_id": current_user["id"]}
    ).sort("created_date", -1)

    orders = []

    async for i in cursor:
        orders.append(
            glovo_document_to_response(i)
        )

    return orders



@order_router.post("/", response_model=OrderResponseSchema)
async def order_create(
    order: OrderCreateSchema,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    store, product = await asyncio.gather(
        get_store(order.store_id),
        get_product(order.product_id)
    )
    print(product)

    if product["store"] != order.store_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The product does not belong to the selected store"
        )


    collection = await get_order_connection()

    total_price = float(product["price"]) * order.quantity
    order_document = {
        "user_id": current_user["id"],

        "store_id": order.store_id,
        "store_name": store["store_name"],

        "product_id": order.product_id,
        "product_name": product["product_name"],

        "category_id": product.get("category_id"),
        "description": product.get("description"),

        "quantity": order.quantity,

        "price": float(product["price"]),
        "total_price": total_price,

        "address": order.address,

        "status": OrderStatus.confirmed.value,

        "created_date": datetime.now(timezone.utc),
        "update_date": datetime.now(timezone.utc),
    }

    result = await collection.insert_one(order_document)

    order_document["_id"] = result.inserted_id


    return glovo_document_to_response(order_document)