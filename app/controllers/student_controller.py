from ..database import db
from bson import ObjectId


# Logique pour récupérer tous les étudiants avec pagination et recherche optionnelle
async def get_all_students(page: int = 1, size: int = 10, name: str = None, s_id: str = None):
    """
    Cette fonction récupère tous les étudiants avec la possibilité de paginer les résultats
    et de filtrer par nom ou identifiant.

    - `page` : Numéro de la page pour la pagination (par défaut 1).
    - `size` : Nombre d'étudiants par page (par défaut 10).
    - `name` : Filtre optionnel pour rechercher un étudiant par nom (insensible à la casse).
    - `s_id` : Filtre optionnel pour rechercher un étudiant par son ID (ObjectId).

    La fonction construit une requête MongoDB dynamique selon les filtres fournis :
    - Si `name` est fourni, il effectue une recherche insensible à la casse via une regex.
    - Si `s_id` est fourni, il cherche l'étudiant par son ID.
    La fonction applique ensuite la pagination via `skip` et `limit`.
    """
    query = {}

    # Si un nom est fourni, on effectue une recherche par expression régulière (insensible à la casse)
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    # Si un identifiant est fourni, on le recherche par ObjectId
    if s_id:
        query["_id"] = ObjectId(s_id)

    # Exécution de la requête MongoDB avec pagination
    students = await db["students"].find(query).skip((page - 1) * size).limit(size).to_list(size)

    # Retourner la liste des étudiants
    return students


# Logique pour récupérer un étudiant spécifique par son ID
async def get_student_by_id(student_id: str):
    """
    Cette fonction récupère un étudiant spécifique en fonction de son identifiant `student_id`.

    - `student_id` : L'identifiant de l'étudiant (ObjectId).

    Elle utilise la méthode `find_one()` pour obtenir un seul document correspondant à l'ID fourni.
    """
    # Récupère un étudiant en cherchant par ObjectId
    student = await db["students"].find_one({"_id": ObjectId(student_id)})

    # Retourne l'étudiant trouvé
    return student


# Logique pour créer un nouvel étudiant
async def create_student(student_data):
    """
    Cette fonction insère un nouvel étudiant dans la base de données.

    - `student_data` : Un dictionnaire contenant les données de l'étudiant à insérer.

    Elle insère les données dans la collection "students" et renvoie l'étudiant nouvellement créé.
    """
    # Insère les données de l'étudiant dans la collection "students"
    result = await db["students"].insert_one(student_data)

    # Récupère l'étudiant fraîchement inséré en utilisant l'ID généré par MongoDB
    student = await db["students"].find_one({"_id": result.inserted_id})

    # Retourner l'étudiant créé
    return student


# Logique pour mettre à jour un étudiant
async def update_student(student_id: str, update_data: dict):
    """
    Cette fonction met à jour un étudiant en fonction de son identifiant `student_id`.

    - `student_id` : L'identifiant de l'étudiant (ObjectId).
    - `update_data` : Un dictionnaire contenant les champs à mettre à jour.

    Elle met à jour uniquement les champs fournis dans `update_data` pour l'étudiant donné.
    """
    # Met à jour les données de l'étudiant dans la collection "students"
    await db["students"].update_one({"_id": ObjectId(student_id)}, {"$set": update_data})

    # Récupère l'étudiant mis à jour pour confirmer les changements
    student = await db["students"].find_one({"_id": ObjectId(student_id)})

    # Retourne l'étudiant mis à jour
    return student


# Logique pour supprimer un étudiant
async def delete_student(student_id: str):
    """
    Cette fonction supprime un étudiant en fonction de son identifiant `student_id`.

    - `student_id` : L'identifiant de l'étudiant (ObjectId).

    Elle supprime le document correspondant dans la base de données et retourne `True`
    si la suppression a réussi, ou `False` sinon.
    """
    # Supprime l'étudiant en fonction de son ObjectId
    result = await db["students"].delete_one({"_id": ObjectId(student_id)})

    # Retourne True si un étudiant a été supprimé, False sinon
    return result
