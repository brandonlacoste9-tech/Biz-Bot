import redis
from app.core.config import settings
from typing import Optional


class RedisService:
    def __init__(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            self.client = None

    def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        if not self.client:
            return None
        try:
            return self.client.get(key)
        except Exception as e:
            print(f"Error getting from Redis: {e}")
            return None

    def set(self, key: str, value: str, expiry: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiry (in seconds)"""
        if not self.client:
            return False
        try:
            if expiry:
                self.client.setex(key, expiry, value)
            else:
                self.client.set(key, value)
            return True
        except Exception as e:
            print(f"Error setting in Redis: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Error deleting from Redis: {e}")
            return False

    def ping(self) -> bool:
        """Check if Redis is available"""
        if not self.client:
            return False
        try:
            return self.client.ping()
        except Exception as e:
            print(f"Error pinging Redis: {e}")
            return False


redis_service = RedisService()
