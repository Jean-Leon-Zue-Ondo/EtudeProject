from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi_jwt_auth import AuthJWT
from ..database import db
from ..schemas import StudentCreate, StudentResponse, StudentUpdate
from ..controllers import student_controller

router = APIRouter()

# Route pour récupérer tous les étudiants avec pagination et recherche optionnelle
@router.get("/", response_model=List[StudentResponse])
async def get_students(page: int = 1, size: int = 10, name: str = None, s_id: str = None):
    students = await student_controller.get_all_students(page, size, name, s_id)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return [
        {
            "id": str(student["_id"]),
            "name": student["name"],
            "email": student["email"],
            "project_ids": student.get("project_ids", [])
        }
        for student in students
    ]

# Route pour récupérer un étudiant par ID
@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    student = await student_controller.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "project_ids": student.get("project_ids", [])
    }

# Route pour créer un nouvel étudiant
@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    student_data = student.dict()
    created_student = await student_controller.create_student(student_data)
    return {
        "id": str(created_student["_id"]),
        "name": created_student["name"],
        "email": created_student["email"],
        "project_ids": created_student.get("project_ids", [])
    }

# Route pour mettre à jour un étudiant
@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student: StudentUpdate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    update_data = student.dict(exclude_unset=True)  # Exclure les champs non envoyés
    updated_student = await student_controller.update_student(student_id, update_data)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": str(updated_student["_id"]),
        "name": updated_student["name"],
        "email": updated_student["email"],
        "project_ids": updated_student.get("project_ids", [])
    }

# Route pour supprimer un étudiant
@router.delete("/{student_id}")
async def delete_student(student_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    deleted = await student_controller.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
