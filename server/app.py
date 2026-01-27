"""Основное приложение aiohttp сервера"""

from aiohttp import web
from . import handlers


def create_app() -> web.Application:
    """Создание и настройка приложения"""
    app = web.Application()

    # Регистрация маршрутов
    app.router.add_get("/health", handlers.health_check)
    app.router.add_post("/data", handlers.create_data)
    app.router.add_get("/data", handlers.list_data)
    app.router.add_get("/data/{id}", handlers.get_data)
    app.router.add_delete("/data/{id}", handlers.delete_data)

    return app


def main():
    """Запуск сервера"""
    app = create_app()
    print("=" * 50)
    print("Culture Analytics API запущен")
    print("URL: http://localhost:8080")
    print("=" * 50)
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
