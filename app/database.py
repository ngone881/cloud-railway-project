from bson.objectid import ObjectId
from fastapi import FastAPI
import asyncio

# Cette variable sera définie dans main.py
product_collection = None

# Helper pour convertir MongoIDs en str
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "quantity": product["quantity"],
        "in_stock": product["in_stock"]
    }

# Initialiser la référence à la collection
def init_db(app: FastAPI):
    global product_collection
    product_collection = app.mongodb.get_collection("products_collection")

# Récupérer tous les produits
async def get_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

# Ajouter un nouveau produit
async def add_product(product_data: dict) -> dict:
    product = await product_collection.insert_one(product_data)
    new_product = await product_collection.find_one({"_id": product.inserted_id})
    return product_helper(new_product)

# Récupérer un produit par ID
async def get_product(id: str) -> dict:
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)

# Mettre à jour un produit
async def update_product(id: str, data: dict):
    if len(data) < 1:
        return False
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        updated_product = await product_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_product:
            return True
        return False

# Supprimer un produit
async def delete_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        await product_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False