# Importation de APIRouter depuis FastAPI
# APIRouter est utilisé pour organiser les routes de manière modulaire dans FastAPI.
# Cela permet de séparer les routes par fonctionnalité, facilitant la gestion du code.
from fastapi import APIRouter

# Importation de la session de base de données depuis le fichier de configuration
# La session permet d'interagir avec la base de données Cassandra via des requêtes CQL (Cassandra Query Language).
from app.config import session

# Importation de uuid4 pour générer un identifiant unique pour chaque projet
# uuid4 génère un identifiant unique au format UUID pour garantir l'unicité des enregistrements dans la base de données.
from uuid import uuid4

# Importation du modèle Project
# Le modèle Project, défini dans un autre fichier, est utilisé pour valider et structurer les données du projet.
from ..models import Project

# Initialisation d'un routeur APIRouter
# Le routeur permet de définir un groupe de routes pour gérer les projets.
router = APIRouter()

# Définition d'une route POST pour créer un projet
# Cette route permet de recevoir les données d'un projet via une requête POST et de les insérer dans la base de données Cassandra.
@router.post("/projects/")
def create_project(project: Project):
    """
    Route POST pour ajouter un nouveau projet à la base de données Cassandra.

    Paramètres :
    - project (Project) : Un objet de type Project contenant les informations du projet (nom, description, date de début, date de fin).

    Retour :
    - Un dictionnaire contenant l'identifiant unique du projet créé et un message de confirmation.
    """
    
    # Génération d'un identifiant unique pour le projet à l'aide de uuid4
    project_id = uuid4()

    # Exécution de la requête CQL pour insérer un nouveau projet dans la table 'projects' de Cassandra
    session.execute(
        """
        INSERT INTO projects (id, name, description, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (project_id, project.name, project.description, project.start_date, project.end_date)  # Insertion des données du projet
    )
    
    # Retourne une réponse JSON avec l'ID du projet et un message de succès
    return {"id": str(project_id), "message": "Project created"}
