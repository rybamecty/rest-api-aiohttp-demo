"""Тесты для сервера"""

import pytest
from server.app import create_app


@pytest.fixture
async def client(aiohttp_client):
    """Фикстура для тестового клиента"""
    app = create_app()
    return await aiohttp_client(app)


async def test_health_check(client):
    """Тест health check endpoint"""
    resp = await client.get("/health")
    assert resp.status == 200

    data = await resp.json()
    assert data["status"] == "ok"
    assert "version" in data


async def test_create_and_get_data(client):
    """Тест создания и получения данных"""
    # Создаем элемент
    create_data = {"name": "Test Item", "value": 123.45}
    resp = await client.post("/data", json=create_data)
    assert resp.status == 201

    created = await resp.json()
    assert "id" in created
    assert created["name"] == "Test Item"
    assert created["value"] == 123.45

    # Получаем созданный элемент
    item_id = created["id"]
    resp = await client.get(f"/data/{item_id}")
    assert resp.status == 200

    fetched = await resp.json()
    assert fetched == created


async def test_list_data(client):
    """Тест получения списка данных"""
    # Создаем несколько элементов
    for i in range(3):
        await client.post(
            "/data",
            json={"name": f"Item {i}", "value": float(i * 100)}
        )

    # Получаем список
    resp = await client.get("/data")
    assert resp.status == 200

    items = await resp.json()
    assert len(items) >= 3


async def test_delete_data(client):
    """Тест удаления данных"""
    # Создаем элемент
    resp = await client.post(
        "/data",
        json={"name": "To Delete", "value": 999.0}
    )
    created = await resp.json()
    item_id = created["id"]

    # Удаляем
    resp = await client.delete(f"/data/{item_id}")
    assert resp.status == 200

    # Проверяем что удален
    resp = await client.get(f"/data/{item_id}")
    assert resp.status == 404


async def test_get_nonexistent_item(client):
    """Тест получения несуществующего элемента"""
    resp = await client.get("/data/99999")
    assert resp.status == 404


async def test_create_invalid_data(client):
    """Тест создания с невалидными данными"""
    resp = await client.post(
        "/data", json={"name": "", "value": 100}  # Пустое имя - невалидно
    )
    assert resp.status == 400
