from fastapi import APIRouter, HTTPException, Depends
import grpc
from src.schemas.auth import (
    TokenResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    RefreshTokenRequest,
    GoogleOAuthRequest,
    OAuthGoogleResponse,
)
from src.infrastructure.grpc.authorization_client import AuthorizationGrpcClient
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.infrastructure.grpc.oauth_client import OAuthGrpcClient
from src.api.dependencies import (
    get_authorization_grpc_client,
    get_user_grpc_client,
    get_oauth_grpc_client,
)

router = APIRouter(tags=["Auth"], responses={200: {"description": "OK"}})

@router.post("/auth/register", response_model=RegisterResponse, responses={200: {"description": "Registered or already exists"}})
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
                name=body.name,
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
            if "avatar_url" in error_msg or "UndefinedColumn" in error_msg:
                raise HTTPException(status_code=503, detail="User profile DB is being updated. Restart user-profile service and retry")
            if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower() or "ALREADY_EXISTS" in error_msg:
                try:
                    existing_profile = await user_client.get_profile_by_id(user_id)
                    if existing_profile.id == user_id:
                        login_result = await auth_client.login(email=body.email, password=body.password)
                        if login_result.get("success"):
                            return {"user_id": user_id, "email": body.email, "access_token": login_result["access_token"], "refresh_token": login_result["refresh_token"], "token_type": "bearer"}
                except HTTPException:
                    raise
                except Exception:
                    pass
            raise HTTPException(status_code=500, detail=f"Failed to create user profile (user_id={user_id}): {error_msg}")
        
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
    except HTTPException:
        raise
    except Exception as e:
        err = str(e)
        if "already exists" in err.lower():
            try:
                login_result = await auth_client.login(email=body.email, password=body.password)
                if login_result.get("success"):
                    return {"user_id": login_result.get("user_id"), "email": body.email, "access_token": login_result["access_token"], "refresh_token": login_result["refresh_token"], "token_type": "bearer"}
            except Exception:
                pass
        raise HTTPException(status_code=400, detail=err)

@router.post("/auth/login", response_model=TokenResponse, responses={200: {"description": "OK"}})
async def login(
    body: LoginRequest,
    auth_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client),
    user_client: UserGrpcClient = Depends(get_user_grpc_client),
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
            "user_id": user_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    responses={
        200: {"description": "OK"},
        400: {"description": "Bad Request"},
        401: {"description": "Invalid or expired refresh token"},
    },
)
async def refresh_token(
    body: RefreshTokenRequest,
    grpc_client: AuthorizationGrpcClient = Depends(get_authorization_grpc_client)
):
    try:
        result = await grpc_client.refresh_token(body.refresh_token)
        if not result["success"]:
            msg = result.get("message", "")
            if "invalid" in msg.lower() or "expired" in msg.lower() or "refresh" in msg.lower():
                raise HTTPException(status_code=401, detail=msg)
            raise HTTPException(status_code=400, detail=msg)
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer",
            "user_id": result.get("user_id"),
        }
    except HTTPException:
        raise
    except Exception as e:
        err = str(e)
        if "invalid" in err.lower() or "expired" in err.lower() or "refresh" in err.lower():
            raise HTTPException(status_code=401, detail=err)
        raise HTTPException(status_code=400, detail=err)


@router.post("/oauth/google/", response_model=OAuthGoogleResponse)
async def google_oauth_sign_in(
    body: GoogleOAuthRequest,
    oauth_client: OAuthGrpcClient = Depends(get_oauth_grpc_client),
):
    try:
        raw_id_token = str(body.idToken or "").strip()
        if raw_id_token.lower().startswith("bearer "):
            raw_id_token = raw_id_token[7:].strip()
        if not raw_id_token:
            raise HTTPException(status_code=400, detail="idToken is required")

        result = await oauth_client.google_sign_in(
            id_token=raw_id_token,
            email=str(body.email or ""),
            name=str(body.name or ""),
            avatar_url=str(body.avatar or ""),
        )
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message", "OAuth sign-in failed"))
        return {
            "access_token": result["access_token"],
            "refresh_token": result["refresh_token"],
            "token_type": "bearer",
            "user_id": result["user_id"],
            "email": result["email"],
            "name": result["name"] or "",
            "avatar": result.get("avatar_url") or None,
            "is_new_user": result.get("is_new_user", False),
        }
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=400, detail=e.details())
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(status_code=503, detail=e.details() or "OAuth service unavailable")
        raise HTTPException(status_code=502, detail=e.details() or "OAuth upstream error")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))