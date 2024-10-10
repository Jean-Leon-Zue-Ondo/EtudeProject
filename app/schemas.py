from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Schéma pour la création d'un étudiant
class StudentCreate(BaseModel):
    """
    Ce schéma est utilisé lors de la création d'un nouvel étudiant.
    - `name` : Le nom de l'étudiant.
    - `email` : L'adresse e-mail de l'étudiant (validation avec `EmailStr`).
    - `course` : Le cours auquel l'étudiant est inscrit (lié au MCD).
    - `branch` : La filière de l'étudiant (lié au MCD).
    """
    name: str
    email: EmailStr
    course: str  # Ajout du champ 'course' pour correspondre au MCD
    branch: str  # Ajout du champ 'branch' pour correspondre au MCD

# Schéma pour la mise à jour d'un étudiant
class StudentUpdate(BaseModel):
    """
    Ce schéma est utilisé pour la mise à jour d'un étudiant existant.
    Tous les champs sont optionnels, permettant de mettre à jour un ou plusieurs champs sans obligation.
    - `name` : Le nom de l'étudiant (optionnel).
    - `email` : L'adresse e-mail de l'étudiant (optionnel).
    - `course` : Le cours de l'étudiant (optionnel).
    - `branch` : La filière de l'étudiant (optionnel).
    """
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    branch: Optional[str]

# Schéma pour la réponse lors de la récupération d'un étudiant
class StudentResponse(BaseModel):
    """
    Ce schéma est utilisé pour la réponse lorsqu'un étudiant est récupéré.
    Il inclut tous les champs d'un étudiant ainsi que les `project_ids` des projets auxquels l'étudiant est inscrit.
    - `id` : Identifiant unique de l'étudiant (ObjectId sous forme de chaîne).
    - `name` : Le nom de l'étudiant.
    - `email` : L'adresse e-mail de l'étudiant.
    - `course` : Le cours de l'étudiant.
    - `branch` : La filière de l'étudiant.
    - `project_ids` : Une liste des projets auxquels l'étudiant est inscrit (ObjectId sous forme de chaînes).
    """
    id: str
    name: str
    email: EmailStr
    course: str  # Ajout du champ 'course' pour la réponse
    branch: str  # Ajout du champ 'branch' pour la réponse
    project_ids: List[str]  # Liste d'ObjectId convertis en chaînes

    class Config:
        from_attributes = True  # Permet d'utiliser des objets ORM avec ce modèle dans Pydantic v2

# Schéma pour la création d'un projet
class ProjectCreate(BaseModel):
    """
    Ce schéma est utilisé lors de la création d'un nouveau projet.
    - `name` : Le nom du projet.
    - `description` : Une description optionnelle du projet.
    - `head` : Le responsable du projet.
    """
    name: str
    description: Optional[str] = None
    head: str  # Ajout du champ 'head' pour correspondre au MCD

# Schéma pour la mise à jour d'un projet
class ProjectUpdate(BaseModel):
    """
    Ce schéma est utilisé pour la mise à jour d'un projet existant.
    Tous les champs sont optionnels, permettant de mettre à jour un ou plusieurs champs.
    - `name` : Le nom du projet (optionnel).
    - `description` : Une description du projet (optionnel).
    - `head` : Le responsable du projet (optionnel).
    """
    name: Optional[str]
    description: Optional[str]
    head: Optional[str]

# Schéma pour la réponse lors de la récupération d'un projet
class ProjectResponse(BaseModel):
    """
    Ce schéma est utilisé pour la réponse lorsqu'un projet est récupéré.
    - `id` : Identifiant unique du projet (ObjectId sous forme de chaîne).
    - `name` : Le nom du projet.
    - `description` : La description du projet.
    - `head` : Le responsable du projet.
    - `student_ids` : Liste des étudiants inscrits dans le projet (ObjectId sous forme de chaînes).
    """
    id: str
    name: str
    description: Optional[str]
    head: str  # Ajout du champ 'head' pour la réponse
    student_ids: List[str]  # Liste d'ObjectId convertis en chaînes

    class Config:
        from_attributes = True  # Permet d'utiliser des objets ORM avec ce modèle dans Pydantic v2

# Schéma pour la création d'un utilisateur
class UserCreate(BaseModel):
    """
    Ce schéma est utilisé lors de la création d'un nouvel utilisateur.
    - `username` : Le nom d'utilisateur.
    - `email` : L'adresse e-mail de l'utilisateur (validation avec `EmailStr`).
    - `password` : Le mot de passe de l'utilisateur (sera haché avant stockage).
    """
    username: str
    email: EmailStr
    password: str  # Ce champ sera haché avant d'être stocké

# Schéma pour la réponse d'un utilisateur
class UserResponse(BaseModel):
    """
    Ce schéma est utilisé pour la réponse lorsqu'un utilisateur est récupéré.
    - `id` : Identifiant unique de l'utilisateur (ObjectId sous forme de chaîne).
    - `username` : Le nom d'utilisateur.
    - `email` : L'adresse e-mail de l'utilisateur.
    - `is_active` : Indique si l'utilisateur est actif.
    - `is_admin` : Indique si l'utilisateur a des privilèges d'administrateur.
    """
    id: str
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # Permet d'utiliser des objets ORM avec ce modèle dans Pydantic v2
