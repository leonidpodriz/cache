from typing import Optional, Type

from cache.key import CacheKey
from cloudflare.entitie import CloudflareList


class CloudflareListCacheKey(CacheKey[CloudflareList]):
    id: Optional[str] = None

    @property
    def target_type(self) -> Type[CloudflareList]:
        return CloudflareList
