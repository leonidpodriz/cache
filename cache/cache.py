from abc import ABC, abstractmethod
from typing import Iterable, Optional, Mapping

from pydantic import BaseModel

from cache.key import CacheKey, CacheValueType


class Cache(ABC):

    @abstractmethod
    def set(self, key: CacheKey, value: BaseModel) -> None:
        pass

    @abstractmethod
    def set_many(self, pairs: Mapping[CacheKey, BaseModel]) -> None:
        pass

    @abstractmethod
    def get(self, key: CacheKey[CacheValueType]) -> Optional[CacheValueType]:
        pass

    @abstractmethod
    def get_many(self, match: CacheKey[CacheValueType]) -> Iterable[CacheValueType]:
        pass
