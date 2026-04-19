from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.crud.product_crud import get_active_products, get_product_by_slug
from app.models.schemas.product import ProductListOut, ProductDetailOut

router = APIRouter()


@router.get("", response_model=List[ProductListOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await get_active_products(db)


@router.get("/{slug}", response_model=ProductDetailOut)
async def get_product(slug: str, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_slug(db, slug)
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    return product
