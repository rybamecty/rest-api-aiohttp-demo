"""Data models for API"""

from pydantic import BaseModel, Field, ConfigDict


class DataItem(BaseModel):
    """Model for data item"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Sales",
                "value": 1000.50
            }
        }
    )

    id: int | None = Field(
        default=None,
        description="Item ID (auto-generated)",
        examples=[1, 2, 3]
    )
    name: str = Field(
        description="Item name",
        min_length=1,
        max_length=100,
        examples=["Sales", "Marketing", "Operations"]
    )
    value: float = Field(
        description="Item value",
        examples=[1000.50, 2500.75, 500.25]
    )


class HealthResponse(BaseModel):
    """Health check response"""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "version": "1.0.0"
            }
        }
    )

    status: str = Field(
        description="Service status",
        examples=["ok", "error", "maintenance"]
    )
    version: str = Field(
        description="API version",
        examples=["1.0.0", "2.0.0", "3.1.0"]
    )


# Дополнительно можно добавить валидаторы
class DataItemCreate(BaseModel):
    """Model for creating data item (without ID)"""

    name: str = Field(
        description="Item name",
        min_length=1,
        max_length=100
    )
    value: float = Field(
        description="Item value",
        ge=0.0  # greater or equal to 0
    )


class DataItemUpdate(BaseModel):
    """Model for updating data item"""

    name: str | None = Field(
        default=None,
        description="Item name",
        min_length=1,
        max_length=100
    )
    value: float | None = Field(
        default=None,
        description="Item value",
        ge=0.0
    )
