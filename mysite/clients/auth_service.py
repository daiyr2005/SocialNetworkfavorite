import httpx
from fastapi import HTTPException, status
from mysite.config import settings
async def verify_access_token(token: str):
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            response = await client.get(f"{settings.auth_service_url}/auth/verify/",
                                        headers={"Authorization":f'Bearer {token}'})
        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Auth service not connection")

        if response.status_code == 401:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token not correct or expired")

        if response.status_code == 201:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Error")

        try:
            user_data = response.json()
            return {
                "id": int(user_data["id"]),
                "username": user_data["username"],
                "user_role": user_data["user_role"],
            }
        except (KeyError, TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Incorrect data")