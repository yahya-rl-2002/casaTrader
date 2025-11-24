"""
Endpoints d'authentification JWT
"""
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_optional,
    TokenData
)
from app.core.config import settings
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Requête de connexion"""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Réponse de connexion"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserInfo(BaseModel):
    """Informations utilisateur"""
    username: str
    user_id: int
    role: Optional[str] = None


@router.post("/login", summary="Login and get JWT token", response_model=LoginResponse)
async def login(login_data: LoginRequest) -> LoginResponse:
    """
    Authentifie un utilisateur et retourne un token JWT
    
    - **username**: Nom d'utilisateur
    - **password**: Mot de passe
    
    **Note**: En production, utiliser une vraie base de données d'utilisateurs.
    """
    user = authenticate_user(login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Créer le token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["user_id"]},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User {user['username']} logged in successfully")
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.get("/me", summary="Get current user info", response_model=UserInfo)
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user)
) -> UserInfo:
    """
    Récupère les informations de l'utilisateur actuellement connecté
    
    Nécessite un token JWT valide dans le header Authorization.
    """
    return UserInfo(
        username=current_user.username or "unknown",
        user_id=current_user.user_id or 0
    )


@router.get("/verify", summary="Verify JWT token")
async def verify_token(
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
) -> dict:
    """
    Vérifie si un token JWT est valide
    
    Retourne les informations de l'utilisateur si le token est valide.
    """
    if current_user is None:
        return {
            "valid": False,
            "message": "No valid token provided"
        }
    
    return {
        "valid": True,
        "username": current_user.username,
        "user_id": current_user.user_id
    }



