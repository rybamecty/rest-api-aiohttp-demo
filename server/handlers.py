"""Обработчики HTTP запросов"""

from aiohttp import web
from typing import Dict
from .models import DataItem, HealthResponse

# Хранилище в памяти
storage: Dict[int, DataItem] = {}
next_id = 1


async def health_check(request: web.Request) -> web.Response:
    """GET /health - Проверка работоспособности сервиса"""
    response = HealthResponse(status="ok", version="1.0.0")
    return web.json_response(response.model_dump())


async def create_data(request: web.Request) -> web.Response:
    """POST /data - Создание нового элемента данных"""
    global next_id

    try:
        data = await request.json()
        item = DataItem(**data)
        item.id = next_id

        storage[next_id] = item
        next_id += 1

        return web.json_response(item.model_dump(), status=201)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)


async def get_data(request: web.Request) -> web.Response:
    """GET /data/{id} - Получение элемента по ID"""
    item_id = int(request.match_info["id"])

    if item_id not in storage:
        return web.json_response({"error": "Item not found"}, status=404)

    item = storage[item_id]
    return web.json_response(item.model_dump())


async def list_data(request: web.Request) -> web.Response:
    """GET /data - Получение списка всех элементов"""
    items = [item.model_dump() for item in storage.values()]
    return web.json_response(items)


async def delete_data(request: web.Request) -> web.Response:
    """DELETE /data/{id} - Удаление элемента"""
    item_id = int(request.match_info["id"])

    if item_id not in storage:
        return web.json_response({"error": "Item not found"}, status=404)

    del storage[item_id]
    return web.json_response({"message": "Deleted successfully"}, status=200)
