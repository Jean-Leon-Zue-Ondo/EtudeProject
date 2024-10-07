# controllers.py ou crud.py

from passlib.context import CryptContext
from bson import ObjectId
from ..database import db  # Assure-toi que cela pointe vers ton fichier de connexion MongoDB

# Créer un contexte pour gérer le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction pour hacher un mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Fonction pour vérifier un mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Créer un nouvel utilisateur
async def create_user(user_data):
    user_data["hashed_password"] = hash_password(user_data["password"])  # Hacher le mot de passe
    del user_data["password"]  # Supprimer le mot de passe en clair avant de le stocker
    result = await db["users"].insert_one(user_data)  # Insérer dans MongoDB
    return await db["users"].find_one({"_id": result.inserted_id})

# Récupérer un utilisateur par son email
async def get_user_by_email(email: str):
    return await db["users"].find_one({"email": email})

# Autres fonctions CRUD...
