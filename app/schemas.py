from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Schéma pour la création d'un étudiant
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str  # Ajout du champ 'course' pour correspondre au MCD
    branch: str  # Ajout du champ 'branch' pour correspondre au MCD

# Schéma pour la mise à jour d'un étudiant
class StudentUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    branch: Optional[str]

# Schéma pour la réponse lors de la récupération d'un étudiant
class StudentResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    course: str  # Ajout du champ 'course' pour la réponse
    branch: str  # Ajout du champ 'branch' pour la réponse
    project_ids: List[str]  # Liste d'ObjectId convertis en chaînes

    class Config:
        from_attributes = True  # Remplace 'orm_mode' dans Pydantic v2

# Schéma pour la création d'un projet
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    head: str  # Ajout du champ 'head' pour correspondre au MCD

# Schéma pour la mise à jour d'un projet
class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    head: Optional[str]

# Schéma pour la réponse lors de la récupération d'un projet
class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    head: str  # Ajout du champ 'head' pour la réponse
    student_ids: List[str]  # Liste d'ObjectId convertis en chaînes

    class Config:
        from_attributes = True  # Remplace 'orm_mode' dans Pydantic v2

# Schéma pour la création d'un utilisateur
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Ce champ sera haché avant d'être stocké

# Schéma pour la réponse d'un utilisateur
class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True