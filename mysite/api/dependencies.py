from mysite.clients.auth_service import verify_access_token
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_schema = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_schema)]):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication credentials were not delivered")
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Bearer access token")

    return await verify_access_token(credentials.credentials)