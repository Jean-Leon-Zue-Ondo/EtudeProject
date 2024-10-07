from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi_jwt_auth import AuthJWT
from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from ..controllers import project_controller

router = APIRouter()

# Route pour récupérer tous les projets avec pagination et recherche optionnelle
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(page: int = 1, size: int = 10, name: str = None, p_id: str = None):
    projects = await project_controller.get_all_projects(page, size, name, p_id)
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")
    return [
        {
            "id": str(project["_id"]),
            "name": project["name"],
            "description": project.get("description", ""),
            "student_ids": [str(student_id) for student_id in project.get("student_ids", [])]
        }
        for project in projects
    ]

# Route pour récupérer un projet par ID
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    project = await project_controller.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": str(project["_id"]),
        "name": project["name"],
        "description": project.get("description", ""),
        "student_ids": [str(student_id) for student_id in project.get("student_ids", [])]
    }

# Route pour créer un nouveau projet
@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    project_data = project.dict()
    created_project = await project_controller.create_project(project_data)
    return {
        "id": str(created_project["_id"]),
        "name": created_project["name"],
        "description": created_project.get("description", ""),
        "student_ids": created_project.get("student_ids", [])
    }

# Route pour mettre à jour un projet
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project: ProjectUpdate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    update_data = project.dict(exclude_unset=True)  # Exclure les champs non envoyés
    updated_project = await project_controller.update_project(project_id, update_data)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": str(updated_project["_id"]),
        "name": updated_project["name"],
        "description": updated_project.get("description", ""),
        "student_ids": updated_project.get("student_ids", [])
    }

# Route pour supprimer un projet
@router.delete("/{project_id}")
async def delete_project(project_id: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Protection par JWT
    deleted = await project_controller.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
