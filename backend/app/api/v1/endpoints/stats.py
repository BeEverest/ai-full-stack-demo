from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.crud.product_crud import get_active_stats
from app.models.schemas.product import StatOut

router = APIRouter()


@router.get("", response_model=List[StatOut])
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await get_active_stats(db)
