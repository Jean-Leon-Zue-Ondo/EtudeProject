# Importation des modules nécessaires depuis FastAPI et les autres fichiers de l'application

from fastapi import FastAPI
# FastAPI est le framework principal utilisé pour construire des API web rapides. FastAPI permet de créer des applications web en Python avec des fonctionnalités comme la validation des données et la documentation automatique.

from .controllers import projects, students
# Importation des contrôleurs "projects" et "students" qui gèrent les routes (endpoints) pour les projets et les étudiants. Ces contrôleurs définissent les routes pour effectuer des opérations CRUD (Créer, Lire, Mettre à jour, Supprimer) sur les projets et les étudiants.

from .auth import router as auth_router
# Importation du routeur d'authentification défini dans "auth.py". Le routeur gère les routes relatives à l'authentification (par exemple, la connexion des utilisateurs et la gestion des tokens JWT).

# Création de l'instance principale de l'application FastAPI
app = FastAPI()
# Cette instance "app" est utilisée pour définir les routes et configurer l'API. C'est l'élément central de toute application FastAPI.

# Inclusion des routes d'authentification via le routeur "auth_router"
app.include_router(auth_router)
# Cette ligne inclut toutes les routes liées à l'authentification dans l'application principale, permettant ainsi à l'utilisateur de se connecter, de récupérer des tokens JWT, etc.

# Inclusion des routes pour projets et étudiants via leurs routeurs respectifs
app.include_router(projects.router)
# Le routeur pour les projets est inclus ici, ce qui permet à l'application d'exposer les endpoints pour créer, lire, modifier et supprimer des projets.

app.include_router(students.router)
# Le routeur pour les étudiants est également inclus ici. Cela expose des routes pour gérer les opérations CRUD sur les étudiants.

# Point de démarrage de l'application
@app.get("/")
# Définition d'une route GET à la racine de l'application. Lorsqu'un utilisateur accède à l'URL racine ("/"), cette fonction est appelée.

def read_root():
    """
    Route de base pour vérifier que l'API fonctionne.
    
    Retourne un simple message JSON pour indiquer que l'API est en ligne.
    """
    return {"message": "API FastAPI avec Cassandra est en ligne"}
    # Retourne un message JSON confirmant que l'API fonctionne correctement. Cette route est souvent utilisée pour vérifier que l'application est démarrée avec succès.
