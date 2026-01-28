"""Tests for the server"""

import pytest
from server.config import create_app


@pytest.fixture
async def client(aiohttp_client):
    """Create test client"""
    app = create_app()
    return await aiohttp_client(app)


async def test_health_check(client):
    """Test health check endpoint"""
    resp = await client.get("/health")
    assert resp.status == 200
    data = await resp.json()
    assert data["status"] == "ok"
    assert "version" in data


async def test_create_and_get_data(client):
    """Test creating and retrieving data"""
    # Create item
    resp = await client.post("/data", json={"name": "Test", "value": 123.45})
    assert resp.status == 201
    data = await resp.json()
    assert data["name"] == "Test"
    assert data["value"] == 123.45
    assert "id" in data

    item_id = data["id"]

    # Get item
    resp = await client.get(f"/data/{item_id}")
    assert resp.status == 200
    data = await resp.json()
    assert data["id"] == item_id
    assert data["name"] == "Test"


async def test_list_data(client):
    """Test listing all data"""
    # Create some items
    await client.post("/data", json={"name": "Item1", "value": 100})
    await client.post("/data", json={"name": "Item2", "value": 200})

    # List all
    resp = await client.get("/data")
    assert resp.status == 200
    data = await resp.json()
    assert len(data) >= 2


async def test_delete_data(client):
    """Test deleting data"""
    # Create item
    resp = await client.post("/data", json={"name": "ToDelete", "value": 999})
    data = await resp.json()
    item_id = data["id"]

    # Delete item
    resp = await client.delete(f"/data/{item_id}")
    assert resp.status == 200

    # Verify deleted
    resp = await client.get(f"/data/{item_id}")
    assert resp.status == 404


async def test_get_nonexistent_item(client):
    """Test getting non-existent item"""
    resp = await client.get("/data/99999")
    assert resp.status == 404
    data = await resp.json()
    assert "error" in data


async def test_create_invalid_data(client):
    """Test creating invalid data"""
    # Missing required field
    resp = await client.post("/data", json={"name": "Test"})
    assert resp.status == 400

    # Invalid value type
    resp = await client.post(
        "/data",
        json={"name": "Test", "value": "not_a_number"}
    )
    assert resp.status == 400
