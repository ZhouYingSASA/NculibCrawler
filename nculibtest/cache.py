from redis import StrictRedis, ConnectionPool


class CacheTool:

    pool = None

    def __init__(self, url):
        self.pool = ConnectionPool.from_url(url)

    def get_connect(self):
        return StrictRedis(connection_pool=self.pool)

    def pop(self):
        return self.get_connect().spop("to_crawl")

    def insert(self, url):
        return self.get_connect().sadd("to_crawl", url)

    def finish_crawl(self, url):
        return self.get_connect().sadd("crawled", url)

    def is_crawled(self, url):
        return bool(self.get_connect().sismember("crawled", url))


cache_tool = CacheTool("redis://:ncuhome@fucheng360.top:6379/0")



