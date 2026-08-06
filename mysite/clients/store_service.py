import httpx

from fastapi import HTTPException, status

from mysite.config import settings



async def get_object(url: str):

    try:

        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

    except httpx.RequestError:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Store service unavailable"
        )


    if response.status_code == 404:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store or product not found"
        )


    if response.status_code != 200:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Store service returned status {response.status_code}"
        )


    try:

        return response.json()

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incorrect data"
        )




async def get_store(store_id: int):

    url = f"{settings.store_service_url}/stores/{store_id}/"

    return await get_object(
        url=url
    )




async def get_product(product_id: int):

    url = f"{settings.store_service_url}/products/{product_id}/"

    return await get_object(
        url=url
    )