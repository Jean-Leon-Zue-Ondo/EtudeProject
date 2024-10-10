from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCreate, UserResponse
from ..controllers import create_user, get_user_by_email
from fastapi_jwt_auth import AuthJWT

# Initialisation du routeur FastAPI
router = APIRouter()


# Route pour l'inscription d'un nouvel utilisateur
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    """
    Cette route permet à un nouvel utilisateur de s'inscrire en fournissant ses informations.
    Elle vérifie si l'utilisateur existe déjà avant de créer un nouveau compte.

    - `user` : Objet Pydantic `UserCreate` contenant les informations de l'utilisateur à créer.
    """

    # Vérifier si l'utilisateur existe déjà en fonction de son email
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        # Si un utilisateur avec cet email existe déjà, lever une erreur HTTP 400
        raise HTTPException(status_code=400, detail="User already exists")

    # Si l'utilisateur n'existe pas, créer un nouvel utilisateur en passant les données au contrôleur
    new_user = await create_user(user.dict())  # Convertir l'objet Pydantic en dictionnaire avant de l'insérer

    # Retourner les informations du nouvel utilisateur sans le mot de passe
    return {
        "id": str(new_user["_id"]),  # Convertir l'ObjectId en chaîne de caractères
        "username": new_user["username"],
        "email": new_user["email"],
        "is_active": new_user["is_active"],  # Statut actif de l'utilisateur
        "is_admin": new_user["is_admin"]  # Indiquer si l'utilisateur a un statut administrateur
    }

# D'autres routes liées aux utilisateurs...
# D'autres routes CRUD (Create, Read, Update, Delete) concernant les utilisateurs
# peuvent être ajoutées ici, comme la mise à jour des informations de l'utilisateur,
# la suppression d'un compte, ou la récupération des détails de l'utilisateur.
