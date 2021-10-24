from abc import ABC, abstractmethod
from typing import Generic, Iterable, Type, TypeVar

from pydantic import BaseModel

CacheValueType = TypeVar('CacheValueType', bound=BaseModel)


class CacheKey(ABC, BaseModel, Generic[CacheValueType]):
    _pattern: str = '%(prefix)s|%(payload)s|'
    _all_char: str = '*'

    def get_values(self) -> Iterable[str]:
        for key, value in self.dict().items():
            if key == 'target_type':
                continue

            if value is None:
                value = self._all_char

            yield str(value)

    def is_fulfilled(self) -> bool:
        for value in self.dict().values():
            if value is None:
                return False

        return True

    @property
    def prefix(self) -> str:
        return self.__class__.__name__

    @property
    def payload(self) -> str:
        return '::'.join(self.get_values())

    @property
    @abstractmethod
    def target_type(self) -> Type[CacheValueType]:
        pass

    def __str__(self) -> str:
        return self._pattern % {
            'prefix': self.prefix,
            'payload': self.payload,
        }
