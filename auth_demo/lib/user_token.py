import heapq
from datetime import datetime, timedelta

from .. import setting
from . import helpers


class Token(object):
    def __init__(self, key, data, expire_time):
        self.key = key
        self.data = data
        self.expire_time = expire_time

    def is_expire(self):
        return self.datetime.now() > self.expire_time

    def __gt__(self, other):
        return self.expire_time > other.expire_time

    def __lt__(self, other):
        return self.expire_time < other.expire_time

    def __eq__(self, other):
        return self.expire_time == other.expire_time


class TokenStore(object):
    _store = {}
    _expire_sort = []
    _last_clear_time = None

    @classmethod
    def create(cls, data):
        key = helpers.random_str(setting.AUTH_TOKEN_SIZE)
        expire_time = datetime.now() + timedelta(hours=setting.AUTH_TOKEN_EXPIRE_HOURS)
        token = Token(key, data, expire_time)
        cls.add(token)
        return token

    @classmethod
    def add(cls, token):
        if token.key in cls._store:
            raise Exception('duplicate key')
        cls.clear_expire()
        cls._store[token.key] = token
        heapq.heappush(token)
        return token

    @classmethod
    def clear_expire(cls):
        if cls._last_clear_time and (datetime.now()-cls._last_clear_time).total_seconds() < 2:
            return
        while cls._expire_sort and cls._expire_sort[0].expire_time < datetime.now():
            token = heapq.heappop(cls._expire_sort)
            cls._store.pop(token.key, None)

    @classmethod
    def get(cls, key):
        token = cls._store.get(key)
        if token and not token.is_expired():
            return token
        return None

    def exists(cls, key):
        token = cls._store.get(key)
        return token and not token.is_expired()

    @classmethod
    def delete(cls, key):
        cls._store.pop(key, None)


