import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_submit_contact_success(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "zhangsan@example.com",
        "inquiry_type": "cooperation",
        "message": "希望与贵公司探讨合作机会",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "24小时" in data["message"]


@pytest.mark.asyncio
async def test_submit_contact_default_inquiry_type(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "李四",
        "email": "lisi@example.com",
        "message": "有问题想咨询",
    })
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_submit_contact_empty_name(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "   ",
        "email": "test@example.com",
        "message": "留言内容",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_invalid_email(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "not-an-email",
        "message": "留言内容",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_empty_message(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "test@example.com",
        "message": "   ",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_message_too_long(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张三",
        "email": "test@example.com",
        "message": "x" * 2001,
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_submit_contact_name_too_long(client: AsyncClient):
    response = await client.post("/api/v1/contact", json={
        "name": "张" * 101,
        "email": "test@example.com",
        "message": "留言内容",
    })
    assert response.status_code == 422
