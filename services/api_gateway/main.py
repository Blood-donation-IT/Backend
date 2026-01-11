import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import settings

from src.api.v1 import auth, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    for kafka 
    """
    print(f"🚀 {settings.APP_NAME} is starting up...")
    yield
    print(f"🛑 {settings.APP_NAME} is shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Gateway service for Blood Donation System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"],      
)

app.add_api_route("/", lambda: {"message": "Welcome to the Blood Donation System API Gateway!"}, tags=["Root"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
# app.include_router(users.router, prefix="/api/v1", tags=["Users"])

# from src.api.v1 import applications
# app.include_router(applications.router, prefix="/api/v1/applications", tags=["Applications"])

# ---  HEALTH CHECK ---
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok", 
        "service": settings.APP_NAME,
        "environment": "development" 
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True 
    )