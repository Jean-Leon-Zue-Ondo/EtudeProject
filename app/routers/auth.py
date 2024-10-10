from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from passlib.context import CryptContext
from pymongo import MongoClient
from starlette import status

# Créer un contexte pour gérer le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = "$2b$12$50o.qQEdtPccEJmje.eb1uNxga8xtzKZxy.JYXdfGPFnJrlMCe9qO"
plain_password = "mdpDawan1234"

if pwd_context.verify(plain_password, hashed_password):
    print("Mot de passe correct")
else:
    print("Mot de passe incorrect")

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["db_EtudiantProject"]  # Remplacez par le nom de votre base de données
users_collection = db["users"]  # Collection MongoDB des utilisateurs

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

# Fonction pour récupérer l'utilisateur par email
def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})

@router.post('/login', response_model=TokenResponse)
async def login(user: Login, Authorize: AuthJWT = Depends()):
    # Chercher l'utilisateur dans la base de données
    user_in_db = get_user_by_email(user.username)

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    #if not user_in_db or not pwd_context.verify(user.password, user_in_db["hashed_password"]):
       # raise HTTPException(status_code=401, detail="Invalid username or password")
    if not user_in_db:
        print("erro email")
    if not pwd_context.verify(user.password, user_in_db["hashed_password"]):
        print("mot de passe incorrect")
    #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Créer le token JWT
    access_token = Authorize.create_access_token(subject=user.username)

    return {"access_token": access_token, "token_type": "bearer"}

# Configurer le JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"  # Vous devez utiliser une clé secrète plus sécurisée en production

@AuthJWT.load_config
def get_config():
    return Settings()
