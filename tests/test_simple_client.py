"""Tests for simple client"""

import pytest
from client.simple_client import CultureAnalyticsClient


@pytest.fixture
def client():
    """Create client instance"""
    return CultureAnalyticsClient(base_url="http://localhost:8080")


async def test_client_health_check(client, aiohttp_server):
    """Test health check through client"""
    from server.config import create_app

    app = create_app()
    server = await aiohttp_server(app)

    client_with_server = CultureAnalyticsClient(
        base_url=f"http://{server.host}:{server.port}"
    )

    response = await client_with_server.health_check()
    assert response["status"] == "ok"
    assert "version" in response


async def test_client_create_and_get_data(client, aiohttp_server):
    """Test creating and getting data through client"""
    from server.config import create_app

    app = create_app()
    server = await aiohttp_server(app)

    client_with_server = CultureAnalyticsClient(
        base_url=f"http://{server.host}:{server.port}"
    )

    # Create item
    created = await client_with_server.create_data(
        name="Client Test",
        value=999.99
    )

    assert created["name"] == "Client Test"
    assert created["value"] == 999.99
    assert "id" in created

    # Get item
    item_id = created["id"]
    fetched = await client_with_server.get_data(item_id)

    assert fetched["id"] == item_id
    assert fetched["name"] == "Client Test"


async def test_client_list_data(client, aiohttp_server):
    """Test listing data through client"""
    from server.config import create_app

    app = create_app()
    server = await aiohttp_server(app)

    client_with_server = CultureAnalyticsClient(
        base_url=f"http://{server.host}:{server.port}"
    )

    # Create some items
    await client_with_server.create_data(name="Item1", value=100)
    await client_with_server.create_data(name="Item2", value=200)

    # List all
    items = await client_with_server.list_data()
    assert len(items) >= 2


async def test_client_delete_data(client, aiohttp_server):
    """Test deleting through client"""
    from server.config import create_app

    app = create_app()
    server = await aiohttp_server(app)

    client_with_server = CultureAnalyticsClient(
        base_url=f"http://{server.host}:{server.port}"
    )

    # Create item
    created = await client_with_server.create_data(name="To Delete", value=123)
    item_id = created["id"]

    # Delete
    result = await client_with_server.delete_data(item_id)
    assert result is not None

    # Verify deleted
    with pytest.raises(ValueError):
        await client_with_server.get_data(item_id)
