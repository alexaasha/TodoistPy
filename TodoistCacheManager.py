import os


class TodoistCacheManager:
    def __init__(self, path_to_cache: str):
        self.path_to_cache = path_to_cache
        self.__cache_existence_flag = True if os.path.exists(path_to_cache) else False

    def is_cache_exists(self):
        return self.__cache_existence_flag

    def get_last_line(self):
        if self.__cache_existence_flag:
            with open(self.path_to_cache) as f:
                last_line = f.readlines()[-1]

            return last_line
        else:
            return ''

    def write(self, data_generator):
        mode = 'a' if self.__cache_existence_flag else 'w'
        with open(self.path_to_cache, mode) as cache:
            cache.writelines(data_generator)

    def remove_cache(self):
        if self.__cache_existence_flag:
            os.remove(self.path_to_cache)

    def read(self, function_to_process):
        try:
            with open(self.path_to_cache) as cache:
                data_generator = function_to_process(list(cache))

            return data_generator
        except FileNotFoundError:
            return iter([])


if __name__ == '__main__':
    cache_manager = TodoistCacheManager('cache.csv')
    data = [("a", 1), ("b", 2)]
    data_gen = map(lambda t: f'{t[0]},{str(t[1])}\n', data)
    cache_manager.write(data_gen)
    func = lambda d: (
        map(lambda t: tuple(t.split(',')),
            map(lambda s: s.strip('\n'), d))
    )
    print(list(cache_manager.read(func)))
