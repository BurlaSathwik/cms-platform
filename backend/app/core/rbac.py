from fastapi import Depends, HTTPException
from app.core.deps import get_current_role
from app.models.user import UserRole


def require_admin(role: UserRole = Depends(get_current_role)):
    if role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return role


def require_editor(role: UserRole = Depends(get_current_role)):
    if role not in [UserRole.admin, UserRole.editor]:
        raise HTTPException(status_code=403, detail="Editor access required")
    return role


def require_viewer(role: UserRole = Depends(get_current_role)):
    if role not in [UserRole.admin, UserRole.editor, UserRole.viewer]:
        raise HTTPException(status_code=403, detail="Viewer access required")
    return role
