import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.domain.product import SiteStat


@pytest.mark.asyncio
async def test_get_stats_empty(client: AsyncClient):
    response = await client.get("/api/v1/stats")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_stats_returns_active_only(client: AsyncClient, db_session: AsyncSession):
    db_session.add(SiteStat(label="专利数量", value="200+", unit="项", sort_order=0, is_active=True))
    db_session.add(SiteStat(label="隐藏数据", value="999", unit="个", sort_order=1, is_active=False))
    await db_session.commit()

    response = await client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["label"] == "专利数量"
    assert data[0]["value"] == "200+"
    assert data[0]["unit"] == "项"


@pytest.mark.asyncio
async def test_get_stats_ordered_by_sort_order(client: AsyncClient, db_session: AsyncSession):
    db_session.add(SiteStat(label="B指标", value="200", unit="个", sort_order=2, is_active=True))
    db_session.add(SiteStat(label="A指标", value="100", unit="项", sort_order=1, is_active=True))
    await db_session.commit()

    response = await client.get("/api/v1/stats")
    data = response.json()
    assert data[0]["label"] == "A指标"
    assert data[1]["label"] == "B指标"
