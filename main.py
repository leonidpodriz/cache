from redis import Redis

from cache.redis import RedisCache
from cloudflare.cache import CloudflareCacheKey, CloudflareItem


def main():
    cache = RedisCache(Redis())
    key = CloudflareCacheKey(group='whitelist', ip='107.233.176.234', id=3)
    match = CloudflareCacheKey(group='whitelist', ip='107.233.176.234')

    value = CloudflareItem(group='whitelist', ip='107.233.176.234', id=3)

    cache.set(key, value)
    result = cache.get(key)
    results = list(cache.get_many(match))
    print(result)
    print(results)


if __name__ == '__main__':
    main()
