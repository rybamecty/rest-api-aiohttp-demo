"""Simple aiohttp client for Culture Analytics API"""

import aiohttp
from typing import Any


class CultureAnalyticsClient:
    """Simple HTTP client for the API"""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()
            self.session = None

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict | None = None,
        expected_statuses: set[int] | int | None = None
    ) -> dict[str, Any]:
        """Internal method to make HTTP requests"""
        if self.session is None:
            async with aiohttp.ClientSession() as session:
                return await self._make_request_with_session(
                    session, method, endpoint, data, expected_statuses
                )
        return await self._make_request_with_session(
            self.session, method, endpoint, data, expected_statuses
        )

    async def _make_request_with_session(
        self,
        session: aiohttp.ClientSession,
        method: str,
        endpoint: str,
        data: dict | None,
        expected_statuses: set[int] | int | None
    ) -> dict[str, Any]:
        """Make request with provided session"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Определяем ожидаемые статусы
        if expected_statuses is None:
            expected_statuses = {200}
        elif isinstance(expected_statuses, int):
            expected_statuses = {expected_statuses}

        async with session.request(method, url, json=data) as response:
            if response.status not in expected_statuses:
                if response.status == 404:
                    raise ValueError(f"Resource not found: {endpoint}")
                text = await response.text()
                raise RuntimeError(
                    f"Request failed: {response.status} - {text}"
                )
            return await response.json()

    async def health_check(self) -> dict[str, Any]:
        """Check API health"""
        return await self._make_request("GET", "/health")

    async def create_data(self, name: str, value: float) -> dict[str, Any]:
        """Create new data item"""
        data = {"name": name, "value": value}
        # Ожидаем 201 Created при успешном создании
        return await self._make_request(
            "POST", "/data", data, expected_statuses={201}
        )

    async def list_data(self) -> list[dict[str, Any]]:
        """Get all data items"""
        return await self._make_request("GET", "/data")

    async def get_data(self, item_id: int) -> dict[str, Any]:
        """Get data item by ID"""
        return await self._make_request("GET", f"/data/{item_id}")

    async def delete_data(self, item_id: int) -> dict[str, Any]:
        """Delete data item by ID"""
        # Ожидаем 200 OK или 204 No Content при успешном удалении
        return await self._make_request("DELETE", f"/data/{item_id}")

    async def update_data(
        self, item_id: int, name: str, value: float
    ) -> dict[str, Any]:
        """Update data item (if API supports it)"""
        data = {"name": name, "value": value}
        return await self._make_request("PUT", f"/data/{item_id}", data)
