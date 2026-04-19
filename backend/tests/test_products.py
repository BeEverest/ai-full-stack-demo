import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.product import Product, ProductFeature, ProductSpec, ProductImage


@pytest.mark.asyncio
async def test_list_products_empty(client: AsyncClient):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_products_returns_active_only(client: AsyncClient, db_session: AsyncSession):
    db_session.add(Product(
        slug="ai-glasses", category="glasses", name="AI眼镜",
        tagline="实时感知", description="描述", cover_image="/img.jpg", is_active=True,
    ))
    db_session.add(Product(
        slug="hidden", category="toy", name="隐藏产品",
        tagline="测试", description="测试", cover_image="/img.jpg", is_active=False,
    ))
    await db_session.commit()

    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["slug"] == "ai-glasses"
    assert data[0]["category"] == "glasses"
    assert data[0]["name"] == "AI眼镜"


@pytest.mark.asyncio
async def test_get_product_detail(client: AsyncClient, db_session: AsyncSession):
    product = Product(
        slug="ai-robot", category="robot", name="AI机器人",
        tagline="智能陪伴", description="详细描述", cover_image="/robot.jpg",
    )
    product.features = [ProductFeature(icon="cpu", title="AI处理", description="本地推理", sort_order=0)]
    product.specs    = [ProductSpec(spec_key="重量", spec_value="1.2kg", sort_order=0)]
    product.images   = [ProductImage(image_url="/r1.jpg", alt_text="正面", sort_order=0)]
    db_session.add(product)
    await db_session.commit()

    response = await client.get("/api/v1/products/ai-robot")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "ai-robot"
    assert data["description"] == "详细描述"
    assert len(data["features"]) == 1
    assert data["features"][0]["title"] == "AI处理"
    assert len(data["specs"]) == 1
    assert data["specs"][0]["spec_key"] == "重量"
    assert len(data["images"]) == 1
    assert data["images"][0]["image_url"] == "/r1.jpg"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/v1/products/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "产品不存在"


@pytest.mark.asyncio
async def test_get_inactive_product_returns_404(client: AsyncClient, db_session: AsyncSession):
    db_session.add(Product(
        slug="inactive", category="toy", name="下架产品",
        tagline="测试", description="测试", cover_image="/img.jpg", is_active=False,
    ))
    await db_session.commit()

    response = await client.get("/api/v1/products/inactive")
    assert response.status_code == 404
