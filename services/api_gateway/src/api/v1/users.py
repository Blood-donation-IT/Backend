from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.user import UserProfileResponse, EditProfileRequest
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.api.dependencies import get_user_grpc_client
from src.core.auth import get_current_user_id

router = APIRouter(tags=["Users"])


@router.get("/users/me", response_model=UserProfileResponse)
async def get_my_profile(
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: UserGrpcClient = Depends(get_user_grpc_client),
):
    try:
        profile = await client.get_profile_by_id(user_id)
        return profile
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User profile not found: {str(e)}")


@router.post("/users/edit_profile", response_model=UserProfileResponse)
async def edit_profile(
    body: EditProfileRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: UserGrpcClient = Depends(get_user_grpc_client),
):
    try:
        profile = await client.update_profile(
            user_id=user_id,
            name=body.name,
            blood_type=body.blood_type,
            avatar_url=body.avatar,
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
