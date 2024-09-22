# Importation de APIRouter depuis FastAPI
# APIRouter permet de créer des routes API dans FastAPI. 
# Cela permet d'organiser les routes en modules séparés pour mieux structurer le projet.
from fastapi import APIRouter

# Importation de la session de base de données depuis le fichier de configuration
# La session est utilisée pour exécuter des requêtes CQL (Cassandra Query Language) dans la base de données Cassandra.
from app.config import session

# Importation de uuid4 pour générer un identifiant unique pour chaque étudiant
# uuid4 génère un identifiant unique aléatoire au format UUID.
from uuid import uuid4

# Importation du modèle Student
# Le modèle Student (défini dans un autre fichier) est utilisé pour la validation des données d'entrée lors de la création d'un étudiant.
from ..models import Student

# Initialisation du routeur APIRouter
# Le routeur permet de définir un groupe de routes pour gérer les étudiants.
router = APIRouter()

# Route POST pour créer un étudiant
# Cette route permet de recevoir les données d'un étudiant via une requête POST et d'insérer ces données dans la base de données Cassandra.
@router.post("/students/")
def create_student(student: Student):
    """
    Route POST pour ajouter un nouvel étudiant à la base de données Cassandra.

    Paramètres :
    - student (Student) : Un objet de type Student contenant les informations de l'étudiant (nom, email, et project_id).

    Retour :
    - Un dictionnaire contenant l'identifiant unique de l'étudiant créé et un message de confirmation.
    """
    # Génération d'un identifiant unique pour l'étudiant à l'aide de uuid4
    student_id = uuid4()

    # Exécution de la requête CQL pour insérer un nouvel étudiant dans la table 'students' de Cassandra
    session.execute(
        """
        INSERT INTO students (id, name, email, project_id)
        VALUES (%s, %s, %s, %s)
        """,
        (student_id, student.name, student.email, student.project_id)  # Insertion des données de l'étudiant
    )
    
    # Retourne une réponse JSON avec l'ID de l'étudiant et un message de succès
    return {"id": str(student_id), "message": "Student created"}
