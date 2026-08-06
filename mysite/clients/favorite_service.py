import httpx

from fastapi import HTTPException, status

from mysite.config import settings



async def get_object(url: str):

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

    except httpx.RequestError:

        raise HTTPException(
            status_code=500,
            detail="Favorite service unavailable"
        )


    if response.status_code == 404:

        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )


    if response.status_code != 200:

        raise HTTPException(
            status_code=503,
            detail="Favorite service error"
        )


    return response.json()



async def get_favorite(user_id:int):

    url = (
        f"{settings.favorite_service_url}"
        f"/favorites/{user_id}"
    )

    return await get_object(url)