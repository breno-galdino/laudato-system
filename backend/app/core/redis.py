import redis
import logging
from .config import settings

logger = logging.getLogger(__name__)


class _SafeRedis:
    """Wrapper around redis.Redis that swallows connection errors.

    When Redis is unavailable every operation returns None/False so the
    application continues to work without cache.
    """

    def __init__(self):
        self._client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    def _call(self, method: str, *args, **kwargs):
        try:
            return getattr(self._client, method)(*args, **kwargs)
        except redis.RedisError as exc:
            logger.warning("Redis unavailable (%s.%s): %s", method, args[:1], exc)
            return None

    def get(self, name):
        return self._call("get", name)

    def set(self, name, value, **kwargs):
        return self._call("set", name, value, **kwargs)

    def setex(self, name, time, value):
        return self._call("setex", name, time, value)

    def delete(self, *names):
        return self._call("delete", *names)

    def exists(self, *names):
        return self._call("exists", *names) or 0


redis_client = _SafeRedis()
