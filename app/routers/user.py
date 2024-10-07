# routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCreate, UserResponse
from ..controllers import create_user, get_user_by_email
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Créer un nouvel utilisateur
    new_user = await create_user(user.dict())
    return {
        "id": str(new_user["_id"]),
        "username": new_user["username"],
        "email": new_user["email"],
        "is_active": new_user["is_active"],
        "is_admin": new_user["is_admin"]
    }

# D'autres routes liées aux utilisateurs...
