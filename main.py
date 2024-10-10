from fastapi import FastAPI
from app.routers import students, projects
from app.database import db
from app.routers import students, projects, auth  # Importer le routeur d'authentification

# Création de l'instance FastAPI
app = FastAPI(
    title="API Etude Project",
    description="API pour gérer les étudiants et projets.",
    version="1.0.0",
    contact={
        "name": "Support EtudeProject",
        "email": "support@etudeproject.com",
    },
)


# Inclure les routes
# Inclure les routeurs pour les différentes sections de l'API
app.include_router(students.router, prefix="/students", tags=["Students"])

# Ce routeur gère les routes liées aux étudiants (création, récupération, mise à jour, suppression).
# Le préfixe "/students" est appliqué à toutes les routes de ce routeur, et un tag "Students" est utilisé pour documenter les routes dans l'API.

app.include_router(projects.router, prefix="/projects", tags=["Projects"])

# Ce routeur gère les routes liées aux projets (ajout, modification, suppression des projets).
# Le préfixe "/projects" est appliqué à toutes les routes de ce routeur, et un tag "Projects" est utilisé pour la documentation.

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Inclure le routeur d'authentification
# Ce routeur gère les routes liées à l'authentification (connexion, déconnexion, gestion des tokens JWT).
# Le préfixe "/auth" est appliqué à toutes les routes de ce routeur, et un tag "Auth" est utilisé pour la documentation.

# Route de base
@app.get("/")
async def root():
    """
    Cette route est accessible via la racine de l'API ("/").
    Elle retourne un simple message de bienvenue pour confirmer que l'API fonctionne.
    """
    return {"message": "Bienvenue sur la plate-forme Etude & Projet"}

# Route de test pour vérifier la connexion MongoDB
@app.get("/test-mongo")
async def test_mongo():
    """
    Cette route permet de tester la connexion avec MongoDB.
    Elle compte le nombre de documents dans la collection 'students' pour vérifier si la base de données est bien connectée.
    En cas de succès, elle retourne un message confirmant la connexion et le nombre d'étudiants dans la base de données.
    En cas d'échec (par exemple, si MongoDB n'est pas accessible), elle retourne une erreur.
    """
    try:
        # Tester la connexion à MongoDB en comptant les documents dans la collection 'students'

        students_count = await db["students"].count_documents({})
        return {"message": "MongoDB is connected", "students_count": students_count}
    except Exception as e:

        # En cas d'erreur, retourner un message d'erreur avec les détails

        return {"error": str(e)}
