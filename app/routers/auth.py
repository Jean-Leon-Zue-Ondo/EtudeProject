from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from passlib.context import CryptContext
from pymongo import MongoClient

# Créer un contexte pour gérer le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Utilisation de passlib pour gérer le hachage des mots de passe avec bcrypt.
# Cela permet de stocker les mots de passe sous forme hachée dans la base de données
# et de vérifier le mot de passe lors de la connexion.

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["db_EtudiantProject"]  # Remplacez par le nom de votre base de données
users_collection = db["users"]  # Collection MongoDB des utilisateurs


# Connexion à une base de données MongoDB appelée "db_EtudiantProject".
# Les utilisateurs sont stockés dans une collection appelée "users".

# Modèle pour la requête de login
class Login(BaseModel):
    username: str
    password: str


# Ce modèle Pydantic définit le format des données attendues pour la connexion.
# L'utilisateur doit fournir un nom d'utilisateur (username) et un mot de passe (password).

# Modèle pour la réponse avec le jeton
class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Ce modèle Pydantic définit la réponse attendue après une connexion réussie.
# La réponse contient un access_token (JWT) et le type de jeton (bearer).

# Créer un routeur FastAPI pour l'authentification
router = APIRouter()


# Le routeur FastAPI permet de regrouper et gérer les routes liées à l'authentification.

# Fonction pour récupérer l'utilisateur par nom d'utilisateur
def get_user_by_username(username: str):
    return users_collection.find_one({"username": username})


# Cette fonction cherche un utilisateur dans la base de données MongoDB
# en fonction du nom d'utilisateur. Elle retourne un document utilisateur s'il est trouvé.

@router.post('/login', response_model=TokenResponse)
async def login(user: Login, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de gérer la connexion d'un utilisateur.
    Elle prend un nom d'utilisateur et un mot de passe, vérifie leur validité
    et renvoie un token JWT si les informations sont correctes.

    - `user` : Un objet du modèle Login qui contient les informations d'authentification.
    - `Authorize` : Dépendance FastAPI pour gérer l'authentification JWT.
    """

    # Chercher l'utilisateur dans la base de données
    user_in_db = get_user_by_username(user.username)
    # Utilise la fonction pour chercher l'utilisateur en fonction du nom d'utilisateur.

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user_in_db or not pwd_context.verify(user.password, user_in_db["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Si l'utilisateur n'existe pas ou que le mot de passe fourni ne correspond pas
    # au mot de passe haché stocké dans la base de données, une exception HTTP 401 (Unauthorized) est levée.

    # Créer le token JWT
    access_token = Authorize.create_access_token(subject=user.username)
    # Si les informations d'authentification sont correctes, un token JWT est généré
    # en utilisant le nom d'utilisateur comme sujet (subject).

    # Retourner le token JWT dans la réponse
    return {"access_token": access_token, "token_type": "bearer"}
    # La réponse contient le token JWT et le type de jeton "bearer" pour les futurs appels API.


# Configurer le JWT
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"  # Utilisez une clé secrète plus sécurisée en production


# Ce modèle Pydantic contient la clé secrète utilisée pour signer et vérifier les tokens JWT.
# Cette clé est utilisée pour sécuriser l'authentification et doit être gardée secrète,
# surtout en production (ici, la valeur est simplement "secret" pour l'exemple).

@AuthJWT.load_config
def get_config():
    return Settings()
# Cette fonction permet de charger la configuration pour JWT, ici en récupérant la clé secrète.
# FastAPI utilise cette configuration pour signer les tokens JWT et les vérifier.
