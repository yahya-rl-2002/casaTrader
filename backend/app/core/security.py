"""
Sécurité et authentification JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# JWT Security
security = HTTPBearer()


class TokenData(BaseModel):
    """Données du token JWT"""
    username: Optional[str] = None
    user_id: Optional[int] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    try:
        # Si le hash est une string, la convertir en bytes
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        if isinstance(plain_password, str):
            plain_password = plain_password.encode('utf-8')
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception as e:
        logger.warning(f"Erreur vérification mot de passe: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash un mot de passe avec bcrypt"""
    # Convertir en bytes si nécessaire
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Générer le salt et hasher
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password, salt)
    # Retourner en string pour stockage
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT
    
    Args:
        data: Données à encoder dans le token
        expires_delta: Durée de vie du token (défaut: 30 minutes)
    
    Returns:
        Token JWT encodé
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Vérifie et décode un token JWT
    
    Args:
        token: Token JWT à vérifier
    
    Returns:
        TokenData si valide, None sinon
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("user_id")
        
        if username is None:
            return None
        
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dépendance FastAPI pour récupérer l'utilisateur actuel depuis le token JWT
    
    Args:
        credentials: Credentials HTTP (Bearer token)
    
    Returns:
        TokenData de l'utilisateur
    
    Raises:
        HTTPException: Si le token est invalide ou manquant
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    return token_data


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[TokenData]:
    """
    Dépendance FastAPI pour récupérer l'utilisateur actuel (optionnel)
    Retourne None si pas de token, au lieu de lever une exception
    
    Args:
        credentials: Credentials HTTP (Bearer token) ou None
    
    Returns:
        TokenData de l'utilisateur ou None
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    return verify_token(token)


# Utilisateurs simples en mémoire (à remplacer par une vraie DB en production)
# En production, utiliser une vraie base de données avec table users
# Note: Le hash est calculé à la première utilisation pour éviter les erreurs d'import
def _get_simple_users():
    """Retourne le dictionnaire des utilisateurs avec mots de passe hashés"""
    return {
        "admin": {
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),  # ⚠️  CHANGER EN PRODUCTION
            "user_id": 1,
            "role": "admin"
        }
    }

# Lazy initialization pour éviter les erreurs d'import
SIMPLE_USERS = None

def get_simple_users():
    """Retourne SIMPLE_USERS, initialisé à la première utilisation"""
    global SIMPLE_USERS
    if SIMPLE_USERS is None:
        SIMPLE_USERS = _get_simple_users()
    return SIMPLE_USERS


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authentifie un utilisateur
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe
    
    Returns:
        Dict avec les infos utilisateur si authentifié, None sinon
    """
    users = get_simple_users()
    user = users.get(username)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return {
        "username": user["username"],
        "user_id": user["user_id"],
        "role": user.get("role", "user")
    }

