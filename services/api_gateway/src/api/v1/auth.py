from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.auth import TokenResponse, LoginRequest, RegisterRequest 
from src.infrastructure.grpc.user_client import UserGrpcClient
from src.api.dependencies import get_user_grpc_client
from src.core.security import create_access_token, get_password_hash, verify_password

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=TokenResponse)
async def register(
    body: RegisterRequest,
    grpc_client: UserGrpcClient = Depends(get_user_grpc_client)
):
    hashed_pw = get_password_hash(body.password)
    
   
    try:
        new_user = await grpc_client.create_user(
            email=body.email, 
            full_name=body.full_name, 
            password_hash=hashed_pw
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User already exists or error {str(e)}")

    access_token = create_access_token(
        data={"sub": str(new_user.id), "roles": [r.value for r in new_user.roles]}
    )
    
    return {"access_token": access_token, "refresh_token": "TODO_LATER", "token_type": "bearer"}

@router.post("/auth/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    grpc_client: UserGrpcClient = Depends(get_user_grpc_client)
):
    
    user_auth_data = await grpc_client.get_auth_data_by_email(email=body.email)
    
    if not user_auth_data:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(body.password, user_auth_data.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_access_token(
        data={"sub": str(user_auth_data.user_id), "roles": user_auth_data.roles}
    )
    
    return {"access_token": access_token, "refresh_token": "TODO", "token_type": "bearer"}