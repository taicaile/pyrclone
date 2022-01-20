"""Redis backend"""
from pyrclone import defaults

from ._queue import Queue
from .utils import assert_package_installed

try:
    import redis
except ImportError:
    redis = "redis"


class RedisQueue(Queue):
    """Redis Queue"""

    def __init__(self, redis_url) -> None:
        super().__init__()
        assert_package_installed(redis)
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

    def push(self, key, filepath):
        """push rclone move task to redis"""
        self.redis_client.sadd(key, filepath)

    def pop(self, key):
        return self.redis_client.spop(key)

    @classmethod
    def from_settings(cls, settings):
        """create backend from settings"""
        redis_url = settings.get("REDIS_URL", defaults.REDIS_URL)
        return cls(redis_url)
