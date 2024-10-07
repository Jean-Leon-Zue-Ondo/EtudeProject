from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from passlib.context import CryptContext

# Créer un contexte pour gérer le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simuler une base de données d'utilisateurs pour l'exemple
fake_users_db = {
    "user@dawan.com": {
        "username": "user@dawan.com",
        "password": pwd_context.hash("Dawan123")  # Hacher le mot de passe
    }
}

# Modèle pour la requête de login
class Login(BaseModel):
    username: str
    password: str

# Modèle pour la réponse avec le jeton
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Créer un routeur FastAPI pour l'authentification
router = APIRouter()

@router.post('/login', response_model=TokenResponse)
async def login(user: Login, Authorize: AuthJWT = Depends()):
    user_in_db = fake_users_db.get(user.username)

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user_in_db or not pwd_context.verify(user.password, user_in_db["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Créer le token JWT
    access_token = Authorize.create_access_token(subject=user.username)

    return {"access_token": access_token, "token_type": "bearer"}

# Configurer le JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()
