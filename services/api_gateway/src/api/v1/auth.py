from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.auth import TokenResponse, LoginRequest, RegisterRequest 
from src.infrastructure.grpc.authorization_client import AuthorizationGrpcClient
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.api.dependencies import get_authorization_grpc_client, get_user_grpc_client

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    auth_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client),
    user_client: UserGrpcClient = Depends(get_user_grpc_client)
):
    try:
        register_result = await auth_client.register(
            email=body.email,
            password=body.password,
            confirm_password=body.confirm_password,
            name=body.name
        )
        
        if not register_result["success"]:
            raise HTTPException(status_code=400, detail=register_result["message"])
        
        user_id = register_result["user_id"]
        
        try:
            await user_client.create_user(
                user_id=user_id,  
                email=body.email,
                full_name=body.name,
                password_hash="", 
                phone=None
            )
        except Exception as profile_error:
            print(f"Warning: Failed to create user profile (user_id={user_id}): {profile_error}")
        
        login_result = await auth_client.login(
            email=body.email,
            password=body.password
        )
        
        if not login_result["success"]:
            raise HTTPException(status_code=400, detail="Registration successful but login failed")
        
        return {
            "access_token": login_result["access_token"],
            "refresh_token": login_result["refresh_token"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User already exists or error {str(e)}")

@router.post("/auth/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    grpc_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client)
):
    try:
        result = await grpc_client.login(
            email=body.email,
            password=body.password
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))