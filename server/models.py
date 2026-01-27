"""Модели данных для API"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class DataItem(BaseModel):
    """Модель элемента данных"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Продажи",
                "value": 1000.50
            }
        }
    )

    id: Optional[int] = Field(None, description="ID элемента")
    name: str = Field(..., description="Название элемента", min_length=1)
    value: float = Field(..., description="Значение")


class HealthResponse(BaseModel):
    """Ответ health check"""

    status: str = Field(..., description="Статус сервиса")
    version: str = Field(..., description="Версия API")
