from fastapi import Depends, HTTPException

def require_role(roles):
    def checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403)
        return user
    return checker
