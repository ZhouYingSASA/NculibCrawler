from redis import StrictRedis, ConnectionPool


class CacheTool:

    pool = None

    def __init__(self, url):
        self.pool = ConnectionPool.from_url(url)

    def get_connect(self):
        return StrictRedis(connection_pool=self.pool)

    def pop(self, key):
        return self.get_connect().spop(key)

    def insert(self, key, url):
        return self.get_connect().sadd(key, url)

    def finish_crawl(self, url):
        return self.get_connect().sadd("crawled", url)

    def is_crawled(self, url):
        return bool(self.get_connect().sismember("crawled", url))


# cache_tool = CacheTool("redis://:ncuhome@fucheng360.top:6379/0")
cache_tool = CacheTool("redis:///localhost:6379/0")


