from typing import Optional, Type

from pydantic import BaseModel

from cache.key import CacheKey


class CloudflareItem(BaseModel):
    ip: Optional[str] = None
    id: Optional[str] = None
    group: Optional[str] = None


class CloudflareCacheKey(CacheKey[CloudflareItem]):
    ip: Optional[str] = None
    id: Optional[str] = None
    group: Optional[str] = None

    @property
    def target_type(self) -> Type[CloudflareItem]:
        return CloudflareItem
