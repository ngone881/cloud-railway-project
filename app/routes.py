from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.database import (
    add_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.models import ProductModel, UpdateProductModel

router = APIRouter()

@router.post("/", response_description="Ajouter un nouveau produit")
async def create_product(product: ProductModel = Body(...)):
    product = jsonable_encoder(product)
    new_product = await add_product(product)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_product)

@router.get("/", response_description="Liste de tous les produits")
async def list_products():
    products = await get_products()
    return {"products": products, "count": len(products)}

@router.get("/{id}", response_description="Récupérer un produit spécifique")
async def find_product(id: str):
    product = await get_product(id)
    if product:
        return product
    raise HTTPException(status_code=404, detail=f"Produit avec l'ID {id} non trouvé")

@router.put("/{id}", response_description="Mettre à jour un produit")
async def update_product_data(id: str, product: UpdateProductModel = Body(...)):
    product = {k: v for k, v in product.dict().items() if v is not None}
    if len(product) >= 1:
        updated_product = await update_product(id, product)
        if updated_product:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"Produit avec l'ID {id} mis à jour"}
            )
    raise HTTPException(status_code=404, detail=f"Produit avec l'ID {id} non trouvé")

@router.delete("/{id}", response_description="Supprimer un produit")
async def delete_product_data(id: str):
    deleted = await delete_product(id)
    if deleted:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Produit avec l'ID {id} supprimé"}
        )
    raise HTTPException(status_code=404, detail=f"Produit avec l'ID {id} non trouvé")