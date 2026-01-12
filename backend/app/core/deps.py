from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_token
from app.models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_role(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    role = payload.get("role")

    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")

    return UserRole(role)
