import hashlib
import inspect
import logging
from typing import NewType, Callable, Tuple, Any, Dict, Optional, List

from kiss_cache.stores.in_memory import InMemoryStore

logger = logging.getLogger(__name__)

DEFAULT_EXPIRATION_TIMEOUT = 60 * 10

KeyExtractor = NewType('KeyExtractor', Callable[[Tuple[Any, ...], Dict[str, Any], Callable[[Any], Any]], Any])
HashExtractor = NewType('HashExtractor', Callable[[str], str])


def default_key_extractor(func: Callable[[Any], str], *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> str:
    return str(args) + str(kwargs) + inspect.getsource(func)


def default_hash_extractor(key: str) -> str:
    m = hashlib.md5()
    m.update(key.encode("utf-8"))
    return m.hexdigest()


class Cache:

    def __init__(self, store=None,
                 key_extractor: KeyExtractor = default_key_extractor,
                 hash_extractor: HashExtractor = default_hash_extractor):
        self.store = store or InMemoryStore()
        self.key_extractor = key_extractor
        self.hash_extractor = hash_extractor

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, expire=DEFAULT_EXPIRATION_TIMEOUT):
        return self.store.set(key, value, expire)

    def memoize(self, expire=DEFAULT_EXPIRATION_TIMEOUT, excluded_keys: Optional[List[str]] = None):

        if excluded_keys is None:
            excluded_keys = []

        def decorator(func):
            def memoized_func(*args, flush: bool = False, **kwargs):

                if excluded_keys:
                    kwargs_for_key = {k: v for k, v in kwargs.items() if k not in excluded_keys}
                else:
                    kwargs_for_key = kwargs

                try:
                    key = self.key_extractor(func, *args, **kwargs_for_key)
                    key = self.hash_extractor(key=key)
                except Exception as e:
                    logger.exception(e)
                    return func(*args, **kwargs)

                if flush is False:
                    value = self.get(key=key)
                else:
                    value = None

                if value is not None:
                    return value

                value = func(*args, **kwargs)
                self.set(key=key, value=value, expire=expire)
                return value

            return memoized_func

        return decorator
