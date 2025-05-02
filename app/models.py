from pydantic import BaseModel, Field
from typing import Optional

class ProductModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    category: str = Field(...)
    quantity: int = Field(...)
    in_stock: bool = Field(default=True)

    class Config:
        schema_extra = {
            "example": {
                "name": "Clavier sans fil Logitech K380",
                "description": "Clavier bluetooth compact multi-dispositifs",
                "price": 55000,
                "category": "périphériques",
                "quantity": 25,
                "in_stock": True
            }
        }

class UpdateProductModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    in_stock: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Clavier sans fil Logitech K380 - Édition Spéciale",
                "price": 65000,
                "quantity": 10
            }
        }

