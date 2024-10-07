from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Créer un client MongoDB et accéder à la base de données
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client["db_EtudiantProject"]
