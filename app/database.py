from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer l'URL de connexion MongoDB à partir des variables d'environnement

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# La fonction `os.getenv()` récupère la variable d'environnement `MONGO_DB_URL`,
# qui contient l'URL de connexion à la base de données MongoDB.
# L'utilisation de dotenv permet de garder les informations sensibles, comme l'URL de la base de données,
# hors du code source, ce qui est plus sécurisé (cela peut inclure des informations d'authentification).

# Créer un client MongoDB asynchrone en utilisant l'URL récupérée
client = AsyncIOMotorClient(MONGO_DB_URL)
# `AsyncIOMotorClient` est le client MongoDB asynchrone fourni par `motor`, une extension asynchrone de `pymongo`.
# Ce client est utilisé pour interagir avec MongoDB dans un environnement asynchrone (par exemple, dans FastAPI).

# Accéder à une base de données spécifique "db_EtudiantProject"

db = client["db_EtudiantProject"]
# La variable `db` permet d'accéder à la base de données MongoDB appelée "db_EtudiantProject".
# Toutes les opérations sur les collections de cette base de données passeront par cet objet.
