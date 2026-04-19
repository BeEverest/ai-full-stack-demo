from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.domain.product import Product, SiteStat


async def get_active_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(
        select(Product)
        .where(Product.is_active == True)
        .order_by(Product.sort_order)
    )
    return list(result.scalars().all())


async def get_product_by_slug(db: AsyncSession, slug: str) -> Product | None:
    result = await db.execute(
        select(Product)
        .where(Product.slug == slug, Product.is_active == True)
        .options(
            selectinload(Product.features),
            selectinload(Product.specs),
            selectinload(Product.images),
        )
    )
    return result.scalar_one_or_none()


async def get_active_stats(db: AsyncSession) -> list[SiteStat]:
    result = await db.execute(
        select(SiteStat)
        .where(SiteStat.is_active == True)
        .order_by(SiteStat.sort_order)
    )
    return list(result.scalars().all())
