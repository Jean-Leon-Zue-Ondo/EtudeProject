# Importation des modules nécessaires pour définir les modèles de données

from pydantic import BaseModel
# Pydantic est une bibliothèque utilisée pour créer des classes de données fortement typées (modèles) dans FastAPI. 
# BaseModel est la classe de base de Pydantic qui permet la validation et la sérialisation des données.

from typing import Optional
# Optional est un type générique utilisé pour indiquer qu'une valeur peut être soit d'un certain type, soit None. 
# Cela permet de rendre certains champs optionnels dans les modèles de données.

from datetime import datetime
# datetime est un module Python intégré qui fournit des classes pour manipuler les dates et heures. 
# Il est utilisé ici pour stocker les informations de date de début et de fin des projets.

# Définition du modèle "Project" qui représente un projet.

class Project(BaseModel):
    """
    Modèle représentant un projet dans l'application.

    Attributs :
    - name (str) : Nom du projet, obligatoire.
    - description (Optional[str]) : Description optionnelle du projet.
    - start_date (datetime) : Date de début du projet, obligatoire.
    - end_date (Optional[datetime]) : Date de fin optionnelle du projet.
    """
    name: str
    # Le nom du projet est un champ obligatoire de type chaîne de caractères (str).
    
    description: Optional[str] = None
    # La description du projet est optionnelle (str ou None). Par défaut, elle est initialisée à None.

    start_date: datetime
    # La date de début du projet est un champ obligatoire, représenté par un objet datetime.

    end_date: Optional[datetime] = None
    # La date de fin du projet est optionnelle (datetime ou None), par défaut None.

# Définition du modèle "Student" qui représente un étudiant.

class Student(BaseModel):
    """
    Modèle représentant un étudiant dans l'application.

    Attributs :
    - name (str) : Nom de l'étudiant, obligatoire.
    - email (str) : Adresse email de l'étudiant, obligatoire.
    - project_id (Optional[str]) : Identifiant du projet auquel l'étudiant est associé, optionnel.
    """
    name: str
    # Le nom de l'étudiant est un champ obligatoire de type chaîne de caractères (str).
    
    email: str
    # L'email de l'étudiant est un champ obligatoire de type chaîne de caractères (str).

    project_id: Optional[str] = None
    # L'ID du projet auquel l'étudiant est associé est optionnel (str ou None), par défaut None.
