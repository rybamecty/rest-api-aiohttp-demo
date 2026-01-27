"""Тесты для простого клиента"""

import pytest
from client.simple_client import CultureAnalyticsClient


@pytest.fixture
def client():
    """Фикстура клиента"""
    return CultureAnalyticsClient(base_url="http://localhost:8080")


async def test_client_health_check(client):
    """Тест health check через клиент"""
    response = await client.health_check()
    assert response["status"] == "ok"
    assert response["version"] == "1.0.0"


async def test_client_create_and_get_data(client):
    """Тест создания и получения данных через клиент"""
    # Создаём элемент
    created = await client.create_data(name="Client Test", value=999.99)

    assert created["name"] == "Client Test"
    assert created["value"] == 999.99
    assert "id" in created

    # Получаем элемент
    item_id = created["id"]
    fetched = await client.get_data(item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == "Client Test"


async def test_client_list_data(client):
    """Тест получения списка через клиент"""
    items = await client.list_data()
    assert isinstance(items, list)


async def test_client_delete_data(client):
    """Тест удаления через клиент"""
    # Создаём элемент
    created = await client.create_data(name="To Delete", value=123)
    item_id = created["id"]

    # Удаляем
    result = await client.delete_data(item_id)
    assert "message" in result
