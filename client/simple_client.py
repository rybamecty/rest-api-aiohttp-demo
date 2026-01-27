"""Простой HTTP клиент для Culture Analytics API"""

import aiohttp
from typing import List, Dict


class CultureAnalyticsClient:
    """Клиент для работы с API"""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url

    async def health_check(self) -> Dict:
        """Проверка работоспособности"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                return await response.json()

    async def create_data(self, name: str, value: float) -> Dict:
        """Создание элемента данных"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/data", json={"name": name, "value": value}
            ) as response:
                return await response.json()

    async def list_data(self) -> List[Dict]:
        """Получение списка всех элементов"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/data") as response:
                return await response.json()


async def get_data(self, item_id: int) -> Dict:
    """Получение элемента по ID"""
    async with aiohttp.ClientSession() as session:
        url = f"{self.base_url}/data/{item_id}"
        async with session.get(url) as response:
            return await response.json()


async def delete_data(self, item_id: int) -> Dict:
    """Удаление элемента"""
    async with aiohttp.ClientSession() as session:
        url = f"{self.base_url}/data/{item_id}"
        async with session.delete(url) as response:
            return await response.json()
