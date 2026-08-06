import httpx

from fastapi import HTTPException

from mysite.config import settings



async def get_story(story_id:int):

    url = (
        f"{settings.story_service_url}"
        f"/stories/{story_id}"
    )


    try:

        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)


    except httpx.RequestError:

        raise HTTPException(
            status_code=500,
            detail="Story service unavailable"
        )


    if response.status_code == 404:

        raise HTTPException(
            status_code=404,
            detail="Story not found"
        )


    return response.json()