from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from fastapi_jwt_auth import AuthJWT
from ..schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from ..controllers import project_controller
from bson import ObjectId

# Initialisation du routeur FastAPI
router = APIRouter()


# Route pour récupérer tous les projets avec pagination et recherche optionnelle
@router.get("/", response_model=List[ProjectResponse])
async def get_projects(page: int = 1, size: int = 10, name: Optional[str] = None, p_id: Optional[str] = None):
    """
    Cette route permet de récupérer tous les projets, avec pagination et une
    possibilité de recherche par nom de projet ou par identifiant de projet.

    - `page` : Numéro de la page pour la pagination (par défaut 1).
    - `size` : Nombre de projets par page (par défaut 10).
    - `name` : Nom du projet pour effectuer une recherche (optionnel).
    - `p_id` : Identifiant du projet pour effectuer une recherche (optionnel).
    """

    # Récupérer les projets depuis le contrôleur, avec pagination et filtres
    projects = await project_controller.get_all_projects(page, size, name, p_id)

    # Si aucun projet n'est trouvé, lever une exception 404
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found")

    # Retourner les projets sous forme de liste de dictionnaires
    return [
        {
            "id": str(project["_id"]),  # Conversion de l'ObjectId en chaîne de caractères
            "name": project["name"],
            "head": project.get("head", ""),  # Récupérer le champ 'head' s'il est présent, sinon valeur par défaut
            "description": project.get("description", ""),  # Récupérer la description ou une chaîne vide par défaut
            "student_ids": [str(student_id) for student_id in project.get("student_ids", [])]
            # Convertir les IDs des étudiants en chaînes
        }
        for project in projects
    ]


# Route pour récupérer un projet par ID
@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Cette route permet de récupérer un projet spécifique par son identifiant `project_id`.

    - `project_id` : L'identifiant du projet à récupérer.
    """

    # Récupérer le projet par son identifiant via le contrôleur
    project = await project_controller.get_project_by_id(project_id)

    # Si le projet n'est pas trouvé, lever une exception 404
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Retourner le projet sous forme de dictionnaire
    return {
        "id": str(project["_id"]),  # Conversion de l'ObjectId en chaîne de caractères
        "name": project["name"],
        "head": project.get("head", ""),  # Récupérer 'head' s'il est présent
        "description": project.get("description", ""),  # Récupérer la description ou une chaîne vide par défaut
        "student_ids": [str(student_id) for student_id in project.get("student_ids", [])]
        # Convertir les IDs des étudiants en chaînes
    }


# Route pour créer un nouveau projet
@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de créer un nouveau projet. Elle est protégée par JWT,
    ce qui signifie que l'utilisateur doit être authentifié.

    - `project` : Le corps de la requête contenant les détails du projet à créer.
    - `Authorize` : Dépendance pour la vérification du JWT (authentification).
    """

    # Vérifie que l'utilisateur est authentifié via JWT
    Authorize.jwt_required()

    # Convertir l'objet Pydantic en dictionnaire
    project_data = project.dict()

    # Créer le projet dans la base de données via le contrôleur
    created_project = await project_controller.create_project(project_data)

    # Retourner les informations du projet créé
    return {
        "id": str(created_project["_id"]),  # Conversion de l'ObjectId en chaîne de caractères
        "name": created_project["name"],
        "head": created_project.get("head", ""),  # Assurer que 'head' est présent ou retourner une chaîne vide
        "description": created_project.get("description", ""),  # Récupérer la description ou une chaîne vide par défaut
        "student_ids": [str(student_id) for student_id in created_project.get("student_ids", [])]
        # Convertir les IDs des étudiants en chaînes
    }


# Route pour mettre à jour un projet
@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project: ProjectUpdate, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de mettre à jour un projet existant par son identifiant `project_id`.
    Elle est protégée par JWT pour vérifier que l'utilisateur est authentifié.

    - `project_id` : L'identifiant du projet à mettre à jour.
    - `project` : Les champs à mettre à jour dans le projet (en excluant ceux qui ne sont pas envoyés).
    - `Authorize` : Dépendance pour la vérification du JWT (authentification).
    """

    # Vérifie que l'utilisateur est authentifié via JWT
    Authorize.jwt_required()

    # Convertir l'objet Pydantic en dictionnaire en excluant les champs non envoyés
    update_data = project.dict(exclude_unset=True)

    # Mettre à jour le projet dans la base de données via le contrôleur
    updated_project = await project_controller.update_project(project_id, update_data)

    # Si le projet n'est pas trouvé, lever une exception 404
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Retourner les informations du projet mis à jour
    return {
        "id": str(updated_project["_id"]),  # Conversion de l'ObjectId en chaîne de caractères
        "name": updated_project["name"],
        "head": updated_project.get("head", ""),  # Assurer que 'head' est présent ou retourner une chaîne vide
        "description": updated_project.get("description", ""),  # Récupérer la description ou une chaîne vide par défaut
        "student_ids": [str(student_id) for student_id in updated_project.get("student_ids", [])]
        # Convertir les IDs des étudiants en chaînes
    }


# Route pour supprimer un projet
@router.delete("/{project_id}")
async def delete_project(project_id: str, Authorize: AuthJWT = Depends()):
    """
    Cette route permet de supprimer un projet par son identifiant `project_id`.
    Elle est protégée par JWT pour s'assurer que l'utilisateur est authentifié.

    - `project_id` : L'identifiant du projet à supprimer.
    - `Authorize` : Dépendance pour la vérification du JWT (authentification).
    """

    # Vérifie que l'utilisateur est authentifié via JWT
    Authorize.jwt_required()

    # Supprimer le projet dans la base de données via le contrôleur
    deleted = await project_controller.delete_project(project_id)

    # Si le projet n'est pas trouvé, lever une exception 404
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

    # Retourner un message confirmant la suppression réussie
    return {"message": "Project deleted successfully"}
