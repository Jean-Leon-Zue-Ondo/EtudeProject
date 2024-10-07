from ..database import db
from bson import ObjectId

# Logique pour récupérer tous les projets avec pagination et recherche optionnelle
async def get_all_projects(page: int = 1, size: int = 10, name: str = None, p_id: str = None):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Recherche par nom avec insensibilité à la casse
    if p_id:
        query["_id"] = ObjectId(p_id)  # Recherche par ID

    projects = await db["projects"].find(query).skip((page - 1) * size).limit(size).to_list(size)
    return projects

# Logique pour récupérer un projet spécifique par son ID
async def get_project_by_id(project_id: str):
    project = await db["projects"].find_one({"_id": ObjectId(project_id)})
    return project

# Logique pour créer un nouveau projet
async def create_project(project_data):
    result = await db["projects"].insert_one(project_data)
    project = await db["projects"].find_one({"_id": result.inserted_id})
    return project

# Logique pour mettre à jour un projet
async def update_project(project_id: str, update_data: dict):
    await db["projects"].update_one({"_id": ObjectId(project_id)}, {"$set": update_data})
    project = await db["projects"].find_one({"_id": ObjectId(project_id)})
    return project

# Logique pour supprimer un projet
async def delete_project(project_id: str):
    result = await db["projects"].delete_one({"_id": ObjectId(project_id)})
    return result.deleted_count == 1
