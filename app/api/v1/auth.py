from fastapi import APIRouter, Depends

from app.api.dependencies.auth import create_access_token

router = APIRouter()


@router.post("/token")
def get_access_token(session_token=Depends(create_access_token)):
    return session_token
