from passlib.context import CryptContext
from bson import ObjectId
from ..database import db  # Assure-toi que cela pointe vers ton fichier de connexion MongoDB

# Créer un contexte pour gérer le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Utilisation de passlib pour gérer le hachage des mots de passe.
# "bcrypt" est l'algorithme de hachage utilisé pour sécuriser les mots de passe.
# `deprecated="auto"` permet de gérer automatiquement la compatibilité des anciens schémas de hachage.

# Fonction pour hacher un mot de passe
def hash_password(password: str) -> str:
    """
    Cette fonction prend un mot de passe en clair et renvoie sa version hachée en utilisant bcrypt.
    """
    return pwd_context.hash(password)


# Fonction pour vérifier un mot de passe
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Cette fonction compare un mot de passe en clair avec un mot de passe haché.

    - `plain_password` : Le mot de passe fourni par l'utilisateur (en clair).
    - `hashed_password` : Le mot de passe haché stocké dans la base de données.

    Retourne True si le mot de passe correspond au mot de passe haché, sinon False.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Créer un nouvel utilisateur
async def create_user(user_data):
    """
    Cette fonction crée un nouvel utilisateur en hachant son mot de passe avant de le stocker.

    - `user_data` : Un dictionnaire contenant les informations de l'utilisateur, y compris le mot de passe.

    Étapes :
    1. Hacher le mot de passe en clair.
    2. Supprimer le mot de passe en clair avant de stocker les données.
    3. Insérer les données de l'utilisateur dans MongoDB.
    4. Récupérer et retourner l'utilisateur fraîchement créé.
    """
    # Hacher le mot de passe et remplacer le mot de passe en clair par sa version hachée
    user_data["hashed_password"] = hash_password(user_data["password"])

    # Supprimer le mot de passe en clair avant d'insérer dans la base de données
    del user_data["password"]

    # Insérer l'utilisateur dans la collection "users" de MongoDB
    result = await db["users"].insert_one(user_data)

    # Retourner l'utilisateur fraîchement créé
    return await db["users"].find_one({"_id": result.inserted_id})


# Récupérer un utilisateur par son email
async def get_user_by_email(email: str):
    """
    Cette fonction récupère un utilisateur en fonction de son adresse email.

    - `email` : L'adresse email de l'utilisateur à rechercher.

    Retourne un document utilisateur s'il est trouvé, sinon None.
    """
    return await db["users"].find_one({"email": email})

# Autres fonctions CRUD...
# D'autres fonctions de gestion CRUD (Create, Read, Update, Delete) peuvent être ajoutées ici
# pour gérer d'autres aspects du modèle utilisateur, comme la mise à jour ou la suppression des utilisateurs.
