import json
from typing import Iterable, Mapping, Optional

from redis import Redis

from .cache import Cache
from .key import CacheKey, CacheValueType


class RedisCache(Cache):
    redis: Redis
    _scan_limit: int = 1000

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    @classmethod
    def validate_set_key(cls, key: CacheKey) -> None:
        if not key.is_fulfilled():
            raise ValueError('Key is not fulfilled!')

    def set(self, key: CacheKey[CacheValueType], value: CacheValueType) -> None:
        assert isinstance(value, key.target_type), 'Target type of key has to be the same as value'
        self.validate_set_key(key)
        self.redis.set(str(key), value.json())

    def set_many(self, pairs: Mapping[CacheKey[CacheValueType], CacheValueType]) -> None:
        self.redis.mset(
            {
                str(key): value.json()
                for key, value
                in pairs.items()
            }
        )

    def get(self, key: CacheKey[CacheValueType]) -> Optional[CacheValueType]:
        raw_value = self.redis.get(str(key))

        if raw_value is None:
            return None

        return key.target_type(**json.loads(raw_value))

    def get_many(self, match: CacheKey[CacheValueType]) -> Iterable[CacheValueType]:
        keys = self.get_keys_match(str(match))
        return (
            match.target_type(**json.loads(value))
            for value in self.redis.mget(keys)
            if isinstance(value, bytes)
        )

    def get_keys_match(self, match: str) -> Iterable[str]:
        for key_bytes in self.get_keys_bytes_by_match(match):
            yield key_bytes.decode()

    def get_keys_bytes_by_match(self, match: str) -> Iterable[bytes]:
        cursor = None

        while cursor != 0:
            cursor, keys = self.redis.scan(cursor or 0, match, self._scan_limit)
            yield from keys
