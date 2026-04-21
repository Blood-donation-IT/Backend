from typing import Annotated

import grpc
from fastapi import APIRouter, HTTPException, Depends

from src.schemas.user import UserProfileResponse, EditProfileRequest
from src.schemas.health_test import (
    GetHealthTestResponse,
    HealthTestQuestionOut,
    PostHealthTestRequest,
    PostHealthTestResponse,
)
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


@router.get("/users/get_test", response_model=GetHealthTestResponse)
async def get_health_test(
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: UserGrpcClient = Depends(get_user_grpc_client),
):
    try:
        data = await client.get_health_test_questions(user_id)
    except grpc.RpcError as e:
        raise HTTPException(status_code=502, detail=e.details())
    return GetHealthTestResponse(
        questions=[
            HealthTestQuestionOut(question_id=q["questionId"], text=q["text"])
            for q in data["questions"]
        ],
        blood_type_options=data["bloodTypeOptions"],
        blood_type_unknown_value=data["bloodTypeUnknownValue"],
    )


@router.post("/users/post_test", response_model=PostHealthTestResponse)
async def post_health_test(
    body: PostHealthTestRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    client: UserGrpcClient = Depends(get_user_grpc_client),
):
    answers_tuples = [(a.question_id, a.value) for a in body.answers]
    try:
        ok, msg = await client.submit_health_test(
            user_id=user_id,
            completed_at=body.completed_at,
            answers=answers_tuples,
            blood_type=body.blood_type,
        )
    except grpc.RpcError as e:
        code = e.code()
        status = 400 if code == grpc.StatusCode.INVALID_ARGUMENT else 502
        raise HTTPException(status_code=status, detail=e.details())
    if not ok:
        raise HTTPException(status_code=400, detail=msg or "Submit failed")
    return PostHealthTestResponse(success=True, message=msg or "OK")
