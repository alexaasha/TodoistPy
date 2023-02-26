import functools


# todo make cache updatable
def cacheable(cache_manager, update_cache=False):
    def decorator_cacheable(f):
        @functools.wraps(f)
        def wrap(*args):
            if cache_manager.is_cache_exists():
                items_dict = cache_manager.read()
            else:
                items_dict = f(*args)

            return items_dict
        return wrap
    return decorator_cacheable
