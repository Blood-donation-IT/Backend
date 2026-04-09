import os
import jwt
import datetime
from typing import Optional, Dict

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ValueError("JWT_SECRET environment variable is not set")
    return secret

class JWTService:
    @staticmethod
    def create_access_token(data: Dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, _get_jwt_secret(), algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: Dict) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, _get_jwt_secret(), algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_token_expires_at(token: str) -> Optional[datetime.datetime]:
        payload = JWTService.verify_token(token)
        if payload and "exp" in payload:
            return datetime.datetime.utcfromtimestamp(payload["exp"])
        return None








