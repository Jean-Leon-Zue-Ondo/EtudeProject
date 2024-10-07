from ..database import db
from bson import ObjectId

# Logique pour récupérer tous les étudiants avec pagination et recherche optionnelle
async def get_all_students(page: int = 1, size: int = 10, name: str = None, s_id: str = None):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Recherche par nom avec insensibilité à la casse
    if s_id:
        query["_id"] = ObjectId(s_id)  # Recherche par ID

    students = await db["students"].find(query).skip((page - 1) * size).limit(size).to_list(size)
    return students

# Logique pour récupérer un étudiant spécifique par son ID
async def get_student_by_id(student_id: str):
    student = await db["students"].find_one({"_id": ObjectId(student_id)})
    return student

# Logique pour créer un nouvel étudiant
async def create_student(student_data):
    result = await db["students"].insert_one(student_data)
    student = await db["students"].find_one({"_id": result.inserted_id})
    return student

# Logique pour mettre à jour un étudiant
async def update_student(student_id: str, update_data: dict):
    await db["students"].update_one({"_id": ObjectId(student_id)}, {"$set": update_data})
    student = await db["students"].find_one({"_id": ObjectId(student_id)})
    return student

# Logique pour supprimer un étudiant
async def delete_student(student_id: str):
    result = await db["students"].delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count == 1
