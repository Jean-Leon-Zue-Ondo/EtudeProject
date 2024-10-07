from fastapi import FastAPI
from app.routers import students, projects
from app.database import db
from app.routers import students, projects, auth  # Importer le routeur d'authentification

app = FastAPI()

# Inclure les routes
# Inclure les routeurs
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])  # Inclure le routeur d'authentification

# Route de base
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI project"}

@app.get("/test-mongo")
async def test_mongo():
    try:
        # Tester la connexion à MongoDB en accédant à la collection 'students'
        students_count = await db["students"].count_documents({})
        return {"message": "MongoDB is connected", "students_count": students_count}
    except Exception as e:
        return {"error": str(e)}