from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from bson import ObjectId


# Gestion de l'ObjectId MongoDB dans Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema.update(type="string")
        return schema

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

# Modèle pour un étudiant
class Student(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    course: str  # Correspond à 's_course' dans le MCD
    branch: str  # Correspond à 's_branch' dans le MCD
    project_ids: Optional[List[str]] = []  # Liste des projets auxquels l'étudiant est inscrit (relation m:n)

    class Config:
        populate_by_name = True  # Remplace 'allow_population_by_field_name' dans Pydantic v2
        json_encoders = {ObjectId: str}  # Pour encoder ObjectId en chaîne
        json_schema_extra = {  # Remplace 'schema_extra' dans Pydantic v2
            "example": {
                "name": "John Doe",
                "course": "Computer Science",
                "branch": "Software Engineering",
                "project_ids": []
            }
        }


# Modèle pour un projet
class Project(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str  # Correspond à 'p_name' dans le MCD
    head: str  # Correspond à 'p_head' dans le MCD (responsable du projet)
    description: Optional[str]
    student_ids: Optional[List[str]] = []  # Liste des étudiants inscrits au projet (relation m:n)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Project A",
                "head": "Dr. Alice",
                "description": "A project description",
                "student_ids": []
            }
        }


class User(BaseModel):
    id: Optional[ObjectId] = None  # MongoDB génère automatiquement l'ID
    username: str
    email: EmailStr
    hashed_password: str  # Stocker le mot de passe sous forme hachée
    is_active: bool = True  # Pour activer/désactiver un utilisateur
    is_admin: bool = False  # Facultatif : pour définir si c'est un admin

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}