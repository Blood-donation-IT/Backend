from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.auth import TokenResponse, LoginRequest, RegisterRequest, RegisterResponse, RefreshTokenRequest 
from src.infrastructure.grpc.authorization_client import AuthorizationGrpcClient
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.api.dependencies import get_authorization_grpc_client, get_user_grpc_client

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=RegisterResponse)
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
            profile_result = await user_client.create_user(
                user_id=user_id,  
                email=body.email,
                full_name=body.name,
                password_hash="", 
                phone=None
            )
        
            if profile_result.id != user_id:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Profile created with different user_id: expected {user_id}, got {profile_result.id}"
                )
            
            verify_profile = await user_client.get_profile_by_id(user_id)
            if verify_profile.id != user_id:
                raise HTTPException(
                    status_code=500,
                    detail=f"Profile verification failed: expected {user_id}, got {verify_profile.id}"
                )
        except HTTPException:
            raise
        except Exception as profile_error:
            error_msg = str(profile_error)
            if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower() or "ALREADY_EXISTS" in error_msg:
                try:
                    existing_profile = await user_client.get_profile_by_id(user_id)
                    if existing_profile.id != user_id:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Existing profile has different user_id: expected {user_id}, got {existing_profile.id}"
                        )
                except HTTPException:
                    raise
                except Exception as get_error:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Profile exists but cannot be retrieved: {str(get_error)}"
                    )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to create user profile (user_id={user_id}): {error_msg}"
                )
        
        login_result = await auth_client.login(
            email=body.email,
            password=body.password
        )
        
        if not login_result["success"]:
            raise HTTPException(status_code=400, detail="Registration successful but login failed")
        
        return {
            "user_id": user_id,
            "email": body.email,
            "access_token": login_result["access_token"],
            "refresh_token": login_result["refresh_token"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User already exists or error {str(e)}")

@router.post("/auth/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    auth_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client),
    user_client: UserGrpcClient = Depends(get_user_grpc_client)
):
    try:
        result = await auth_client.login(
            email=body.email,
            password=body.password
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        user_id = result.get("user_id")
        

        profile_exists = False
        try:
            profile = await user_client.get_profile_by_id(user_id)
            profile_exists = True
        except Exception:
            profile_exists = False
         
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    body: RefreshTokenRequest,
    grpc_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client)
):
    try:
        result = await grpc_client.refresh_token(body.refresh_token)

        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))