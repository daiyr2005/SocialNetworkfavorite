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
            detail="Post service unavailable"
        )


    if response.status_code == 404:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )


    if response.status_code != 200:

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Post service returned {response.status_code}"
        )


    try:
        return response.json()

    except ValueError:

        raise HTTPException(
            status_code=500,
            detail="Incorrect post data"
        )



async def get_post(post_id: int):

    url = (
        f"{settings.post_service_url}"
        f"/posts/{post_id}/"
    )

    return await get_object(url)