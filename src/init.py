from src.config import settings
from src.connectors.redis_connector import RegisManager

redis_manager = RegisManager(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT
    )
