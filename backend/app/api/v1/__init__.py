from fastapi import APIRouter
from app.api.v1.endpoints import products, contact, stats

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(contact.router,  prefix="/contact",  tags=["contact"])
api_router.include_router(stats.router,    prefix="/stats",    tags=["stats"])
