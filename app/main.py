import os
from fastapi import FastAPI
from app.routes import router as product_router
import uvicorn
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from app.database import init_db

# Charger les variables d'environnement
load_dotenv()

# Lire les variables depuis le fichier .env
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_db_name = os.getenv("MONGO_DB_NAME", "products")

# Construire l'URI MongoDB dynamiquement avec username et password
mongo_uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.j1p1zn6.mongodb.net/{mongo_db_name}?retryWrites=true&w=majority&appName=Cluster0"

# Créer l'application FastAPI
app = FastAPI(
    title="NgoneShop API",
    description="API pour la gestion des produits informatiques de NgoneShop qui est une boutique en ligne",
    version="1.0.0"
)

# Connexion à MongoDB
@app.on_event("startup")
async def startup_db():
    app.mongodb_client = AsyncIOMotorClient(mongo_uri)
    app.mongodb = app.mongodb_client[mongo_db_name]
    # Initialiser la référence à la collection dans database.py
    init_db(app)

@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()

# Inclure le routeur
app.include_router(product_router, tags=["Products"], prefix="/api/products")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenue dans l'API de NgoneShop!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Utilise la variable d'environnement PORT ou 8000 par défaut
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)