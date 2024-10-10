from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi_jwt_auth import AuthJWT
from ..database import db
from ..schemas import StudentCreate, StudentResponse, StudentUpdate
from ..controllers import student_controller

router = APIRouter()  # Crée un routeur FastAPI pour regrouper les routes liées aux étudiants

# Route pour récupérer tous les étudiants avec pagination et recherche optionnelle
@router.get("/", response_model=List[StudentResponse])
async def get_students(page: int = 1, size: int = 10, name: str = None, s_id: str = None):
    """
    Cette route permet de récupérer une liste d'étudiants avec pagination et recherche optionnelle
    par nom ou identifiant.
    """
    students = await student_controller.get_all_students(page, size, name, s_id)  # Récupérer les étudiants depuis le contrôleur
    if not students:
        # Si aucun étudiant n'est trouvé, lever une erreur HTTP 404
        raise HTTPException(status_code=404, detail="No students found")

    # Retourner la liste d'étudiants avec les champs formatés correctement
    return [
        {
            "id": str(student["_id"]),  # Convertir l'ObjectId en chaîne de caractères
            "name": student.get("name", ""),  # Assurer que 'name' est présent
            "email": student.get("email", ""),  # Assurer que 'email' est présent ou mettre une valeur par défaut
            "course": student.get("course", ""),  # Assurer que 'course' est présent
            "branch": student.get("branch", ""),  # Assurer que 'branch' est présent
            # Convertir 'project_ids' en liste de chaînes si ce n'est pas déjà le cas
            "project_ids": [str(pid) for pid in student.get("project_ids", []) if isinstance(pid, ObjectId)]
        }
        for student in students  # Boucle sur chaque étudiant dans la liste récupérée
    ]

# Route pour récupérer un étudiant par ID
@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    """
    Cette route permet de récupérer un étudiant spécifique par son identifiant MongoDB.
    """
    student = await student_controller.get_student_by_id(student_id)  # Récupérer l'étudiant par son ID
    if not student:
        # Si l'étudiant n'est pas trouvé, lever une erreur HTTP 404
        raise HTTPException(status_code=404, detail="Student not found")

    # Retourner les informations de l'étudiant trouvé
    return {
        "id": str(student["_id"]),  # Convertir l'ObjectId en chaîne de caractères
        "name": student.get("name", ""),  # Assurer que 'name' est présent
        "email": student.get("email", ""),  # Assurer que 'email' est présent ou mettre une valeur par défaut
        "course": student.get("course", ""),  # Assurer que 'course' est présent
        "branch": student.get("branch", ""),  # Assurer que 'branch' est présent
        # Convertir 'project_ids' en liste de chaînes si ce n'est pas déjà le cas
        "project_ids": [str(pid) for pid in student.get("project_ids", []) if isinstance(pid, ObjectId)]
    }

# Route pour créer un nouvel étudiant
@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de créer un nouvel étudiant. Elle est protégée par JWT.
    """
    Authorize.jwt_required()  # Vérifie que l'utilisateur est authentifié via JWT
    student_data = student.dict()  # Convertir l'objet Pydantic en dictionnaire
    created_student = await student_controller.create_student(student_data)  # Créer l'étudiant dans la base de données

    # Retourner les informations de l'étudiant créé
    return {
        "id": str(created_student["_id"]),  # Convertir l'ObjectId en chaîne de caractères
        "name": created_student["name"],
        "email": created_student.get("email", ""),  # Assurer que 'email' est présent
        "course": created_student.get("course", ""),  # Assurer que 'course' est présent
        "branch": created_student.get("branch", ""),  # Assurer que 'branch' est présent
        # Convertir 'project_ids' en liste de chaînes si ce n'est pas déjà le cas
        "project_ids": [str(pid) for pid in created_student.get("project_ids", []) if isinstance(pid, ObjectId)]
    }

# Route pour mettre à jour un étudiant
@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student: StudentUpdate, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de mettre à jour les informations d'un étudiant. Elle est protégée par JWT.
    """
    Authorize.jwt_required()  # Vérifie que l'utilisateur est authentifié via JWT
    update_data = student.dict(exclude_unset=True)  # Convertir l'objet Pydantic en dictionnaire, excluant les champs non envoyés
    updated_student = await student_controller.update_student(student_id, update_data)  # Mettre à jour l'étudiant dans la base de données

    if not updated_student:
        # Si l'étudiant n'est pas trouvé, lever une erreur HTTP 404
        raise HTTPException(status_code=404, detail="Student not found")

    # Retourner les informations de l'étudiant mis à jour
    return {
        "id": str(updated_student["_id"]),  # Convertir l'ObjectId en chaîne de caractères
        "name": updated_student["name"],
        "email": updated_student.get("email", ""),  # Assurer que 'email' est présent
        "course": updated_student.get("course", ""),  # Assurer que 'course' est présent
        "branch": updated_student.get("branch", ""),  # Assurer que 'branch' est présent
        # Convertir 'project_ids' en liste de chaînes si ce n'est pas déjà le cas
        "project_ids": [str(pid) for pid in updated_student.get("project_ids", []) if isinstance(pid, ObjectId)]
    }

# Route pour supprimer un étudiant
@router.delete("/{student_id}")
async def delete_student(student_id: str, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de supprimer un étudiant. Elle est protégée par JWT.
    """
    Authorize.jwt_required()  # Vérifie que l'utilisateur est authentifié via JWT
    deleted = await student_controller.delete_student(student_id)  # Supprimer l'étudiant dans la base de données

    if not deleted:
        # Si l'étudiant n'est pas trouvé, lever une erreur HTTP 404
        raise HTTPException(status_code=404, detail="Student not found")

    # Retourner un message de succès une fois l'étudiant supprimé
    return {"message": "Student deleted successfully"}
