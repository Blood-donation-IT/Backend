from fastapi import APIRouter, HTTPException, Depends
from src.schemas.user import UserProfileResponse
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.api.dependencies import get_user_grpc_client

router = APIRouter(tags=["Users"])

@router.get("/users/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int,
    client: UserGrpcClient = Depends(get_user_grpc_client)
):
    try:
        profile = await client.get_profile_by_id(user_id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User profile not found: {str(e)}")
