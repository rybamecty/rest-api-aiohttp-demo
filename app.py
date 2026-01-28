"""Main application entry point"""
import logging
from aiohttp import web

from server.config import create_app, config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Run the application"""
    app = create_app()
    
    logger.info(f"Starting server on {config.base_url}")
    logger.info("Available endpoints:")
    logger.info(f"  GET  {config.base_url}/health - Health check")
    logger.info(f"  POST {config.base_url}/data - Create item")
    logger.info(f"  GET  {config.base_url}/data - List all items")
    logger.info(f"  GET  {config.base_url}/data/{{id}} - Get item by ID")
    logger.info(f"  DELETE {config.base_url}/data/{{id}} - Delete item")
    
    web.run_app(app, host=config.HOST, port=config.PORT)


if __name__ == '__main__':
    main()
