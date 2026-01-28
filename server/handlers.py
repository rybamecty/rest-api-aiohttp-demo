"""HTTP request handlers"""

import logging
from http import HTTPStatus
from typing import Final

from aiohttp import web
from pydantic import ValidationError

from server.models import DataItem, HealthResponse
from server.config import config

# Setup logging
logger: Final = logging.getLogger(__name__)

# In-memory storage
storage: dict[int, DataItem] = {}
next_id: int = 1


def _error_response(
    message: str,
    status: HTTPStatus,
    details: list[dict] | None = None
) -> web.Response:
    """Helper for error responses"""
    response_data = {"error": message}
    if details:
        response_data["details"] = details

    return web.json_response(
        response_data,
        status=status
    )


async def health_check(request: web.Request) -> web.Response:
    """Health check endpoint"""
    logger.info("Health check requested")

    health = HealthResponse(
        status="ok",
        version=config.API_VERSION
    )
    return web.json_response(
        health.model_dump(),
        status=HTTPStatus.OK
    )


async def create_data(request: web.Request) -> web.Response:
    """Create new data item"""
    global next_id

    try:
        data = await request.json()
        logger.info(f"Creating new item: {data}")

        item = DataItem(**data)
        item.id = next_id
        storage[next_id] = item
        next_id += 1

        logger.info(f"Item created successfully with id={item.id}")
        return web.json_response(
            item.model_dump(),
            status=HTTPStatus.CREATED
        )

    except ValidationError as e:
        logger.warning(f"Validation error: {e}")
        return _error_response(
            "Invalid data",
            HTTPStatus.BAD_REQUEST,
            e.errors()
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return _error_response(
            "Internal server error",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )


async def list_data(request: web.Request) -> web.Response:
    """Get all data items"""
    count = len(storage)
    logger.info(f"Listing all items, total count: {count}")

    items = [item.model_dump() for item in storage.values()]
    return web.json_response(items, status=HTTPStatus.OK)


async def get_data(request: web.Request) -> web.Response:
    """Get data item by ID"""
    item_id = int(request.match_info["id"])
    logger.info(f"Retrieving item with id={item_id}")

    if item_id not in storage:
        logger.warning(f"Item with id={item_id} not found")
        return _error_response(
            f"Item with id {item_id} not found",
            HTTPStatus.NOT_FOUND
        )

    item = storage[item_id]
    return web.json_response(
        item.model_dump(),
        status=HTTPStatus.OK
    )


async def delete_data(request: web.Request) -> web.Response:
    """Delete data item by ID"""
    item_id = int(request.match_info["id"])
    logger.info(f"Deleting item with id={item_id}")

    if item_id not in storage:
        logger.warning(f"Item with id={item_id} not found")
        return _error_response(
            f"Item with id {item_id} not found",
            HTTPStatus.NOT_FOUND
        )

    del storage[item_id]
    logger.info(f"Item with id={item_id} deleted successfully")
    return web.json_response(
        {"message": "Item deleted"},
        status=HTTPStatus.OK
    )
