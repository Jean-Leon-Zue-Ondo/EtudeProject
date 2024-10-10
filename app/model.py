from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId

# Gestion de l'ObjectId MongoDB dans Pydantic v2
class PyObjectId(ObjectId):
    """
    Cette classe permet de gérer la conversion entre l'ObjectId de MongoDB et Pydantic.
    MongoDB utilise un type ObjectId spécifique pour les identifiants de documents,
    mais Pydantic ne gère pas ce type nativement. PyObjectId permet de valider et de convertir les ObjectId en chaînes.
    """

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        """
        Cette méthode permet de définir comment Pydantic doit interpréter un ObjectId lorsqu'il génère des schémas JSON.
        Elle met à jour le schéma pour indiquer que l'ObjectId doit être traité comme une chaîne de caractères.
        """
        schema.update(type="string")
        return schema

    @classmethod
    def __get_validators__(cls):
        """
        Cette méthode fournit un validateur pour l'ObjectId.
        Le validateur sera utilisé pour s'assurer que les valeurs passées dans un champ ObjectId sont valides.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Valide si la valeur fournie est un ObjectId MongoDB valide.
        Si ce n'est pas le cas, une erreur sera levée.
        """
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)


# Modèle pour un étudiant
class Student(BaseModel):
    """
    Ce modèle Pydantic représente un étudiant dans le système.
    - `id`: Un identifiant unique généré par MongoDB.
    - `name`: Le nom de l'étudiant.
    - `course`: Le cours auquel l'étudiant est inscrit.
    - `branch`: La filière à laquelle l'étudiant est associé.
    - `project_ids`: Une liste d'identifiants de projets auxquels l'étudiant est inscrit (relation m:n).
    """
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")  # Utilise PyObjectId pour gérer l'ObjectId
    name: str
    course: str  # Correspond au champ 's_course' du modèle conceptuel de données (MCD)
    branch: str  # Correspond au champ 's_branch' du MCD
    project_ids: Optional[List[str]] = []  # Liste des projets, par défaut vide

    class Config:
        populate_by_name = True  # Permet l'utilisation de noms alternatifs pour les champs
        json_encoders = {ObjectId: str}  # Indique à Pydantic d'encoder ObjectId en tant que chaîne
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "course": "Computer Science",
                "branch": "Software Engineering",
                "project_ids": []  # Exemple de liste de projets vide
            }
        }


# Modèle pour un projet
class Project(BaseModel):
    """
    Ce modèle Pydantic représente un projet dans le système.
    - `id`: Un identifiant unique généré par MongoDB.
    - `name`: Le nom du projet.
    - `head`: Le responsable du projet.
    - `description`: Une description optionnelle du projet.
    - `student_ids`: Une liste d'identifiants d'étudiants inscrits au projet (relation m:n).
    """
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")  # Utilise PyObjectId pour gérer l'ObjectId
    name: str  # Nom du projet
    head: str  # Responsable du projet (p_head dans le MCD)
    description: Optional[str]  # Description optionnelle du projet
    student_ids: Optional[List[str]] = []  # Liste des étudiants inscrits

    class Config:
        populate_by_name = True  # Permet l'utilisation de noms alternatifs pour les champs
        json_encoders = {ObjectId: str}  # Indique à Pydantic d'encoder ObjectId en tant que chaîne
        json_schema_extra = {
            "example": {
                "name": "Project A",
                "head": "Dr. Alice",
                "description": "A project description",  # Exemple de description du projet
                "student_ids": []  # Exemple de liste d'étudiants vide
            }
        }


# Modèle pour un utilisateur
class User(BaseModel):
    """
    Ce modèle Pydantic représente un utilisateur dans le système.
    - `id`: Un identifiant unique généré par MongoDB.
    - `username`: Le nom d'utilisateur.
    - `email`: L'adresse e-mail de l'utilisateur.
    - `hashed_password`: Le mot de passe haché.
    - `is_active`: Indique si l'utilisateur est actif.
    - `is_admin`: Indique si l'utilisateur a des privilèges d'administrateur.
    """
    id: Optional[ObjectId] = None  # MongoDB génère automatiquement l'ID si ce n'est pas fourni
    username: str  # Nom d'utilisateur
    email: EmailStr  # Adresse e-mail validée (EmailStr est une classe Pydantic pour valider les e-mails)
    hashed_password: str  # Mot de passe haché
    is_active: bool = True  # Statut actif de l'utilisateur, par défaut True
    is_admin: bool = False  # Statut administrateur, par défaut False

    class Config:
        allow_population_by_field_name = True  # Permet l'utilisation de noms alternatifs pour les champs
        json_encoders = {ObjectId: str}  # Indique à Pydantic d'encoder ObjectId en tant que chaîne
