from ..database import db
from bson import ObjectId


# Logique pour récupérer tous les projets avec pagination et recherche optionnelle
async def get_all_projects(page: int = 1, size: int = 10, name: str = None, p_id: str = None):
    """
    Cette fonction récupère tous les projets depuis la base de données, avec des options
    de pagination et de recherche.

    - `page` : Numéro de la page pour la pagination (par défaut 1).
    - `size` : Nombre de projets à retourner par page (par défaut 10).
    - `name` : Filtre optionnel pour rechercher un projet par nom (insensible à la casse).
    - `p_id` : Filtre optionnel pour rechercher un projet par son ID (MongoDB ObjectId).

    La fonction construit une requête MongoDB dynamique selon les filtres fournis :
    - Si `name` est fourni, on effectue une recherche par nom avec insensibilité à la casse (regex).
    - Si `p_id` est fourni, on cherche par l'identifiant du projet (ObjectId).
    La fonction applique ensuite la pagination avec `skip` et `limit`.
    """
    query = {}

    # Recherche par nom de projet avec une expression régulière (insensible à la casse)
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    # Recherche par identifiant de projet (conversion en ObjectId)
    if p_id:
        query["_id"] = ObjectId(p_id)

    # Exécution de la requête avec pagination
    projects = await db["projects"].find(query).skip((page - 1) * size).limit(size).to_list(size)

    # Retourne la liste des projets récupérés
    return projects


# Logique pour récupérer un projet spécifique par son ID
async def get_project_by_id(project_id: str):
    """
    Cette fonction récupère un projet spécifique en fonction de son identifiant `project_id`.

    - `project_id` : L'identifiant du projet (doit être converti en ObjectId).

    La fonction utilise `find_one` pour rechercher un seul projet correspondant à l'ID.
    """
    project = await db["projects"].find_one({"_id": ObjectId(project_id)})

    # Retourne le projet correspondant
    return project


# Logique pour créer un nouveau projet
async def create_project(project_data):
    """
    Cette fonction insère un nouveau projet dans la base de données.

    - `project_data` : Un dictionnaire contenant les données du projet à créer.

    La fonction insère les données dans la collection "projects" et renvoie le projet créé.
    """
    # Insère le projet dans la collection "projects"
    result = await db["projects"].insert_one(project_data)

    # Récupère le projet fraîchement inséré en utilisant l'ID généré
    project = await db["projects"].find_one({"_id": result.inserted_id})

    # Retourne le projet créé
    return project


# Logique pour mettre à jour un projet
async def update_project(project_id: str, update_data: dict):
    """
    Cette fonction met à jour un projet spécifique en fonction de son identifiant.

    - `project_id` : L'identifiant du projet (doit être converti en ObjectId).
    - `update_data` : Un dictionnaire contenant les données à mettre à jour.

    La fonction met à jour les champs spécifiés dans `update_data` pour le projet donné.
    """
    # Mise à jour du projet dans la collection "projects"
    await db["projects"].update_one({"_id": ObjectId(project_id)}, {"$set": update_data})

    # Récupère le projet mis à jour
    project = await db["projects"].find_one({"_id": ObjectId(project_id)})

    # Retourne le projet mis à jour
    return project


# Logique pour supprimer un projet
async def delete_project(project_id: str):
    """
    Cette fonction supprime un projet spécifique en fonction de son identifiant `project_id`.

    - `project_id` : L'identifiant du projet (doit être converti en ObjectId).

    La fonction supprime le projet correspondant dans la base de données et retourne `True` si la suppression a réussi.
    """
    # Suppression du projet dans la collection "projects"
    result = await db["projects"].delete_one({"_id": ObjectId(project_id)})

    # Retourne True si un document a été supprimé, False sinon
    return result.deleted_count == 1
