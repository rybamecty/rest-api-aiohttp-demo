"""Configuration settings for the application"""

import os
from aiohttp import web


class Config:
    """Application configuration"""
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8080))

    # API settings
    API_VERSION = "1.0.0"

    @property
    def base_url(self):
        """Get base URL for the application"""
        return f"http://{self.HOST}:{self.PORT}"


# Global config instance
config = Config()


def create_app() -> web.Application:
    """Create and configure aiohttp application"""
    # Import here to avoid circular imports
    from server import handlers

    app = web.Application()

    # Register routes
    app.router.add_get("/health", handlers.health_check)
    app.router.add_post("/data", handlers.create_data)
    app.router.add_get("/data", handlers.list_data)
    app.router.add_get("/data/{id}", handlers.get_data)
    app.router.add_delete("/data/{id}", handlers.delete_data)

    return app
