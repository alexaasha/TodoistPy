import os
import json


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

    def write(self, data_dict: dict):
        with open(self.path_to_cache, 'w') as f:
            json.dump(data_dict, f, indent='  ')

    def remove_cache(self):
        if self.__cache_existence_flag:
            os.remove(self.path_to_cache)

    def read(self) -> dict:
        with open(self.path_to_cache, 'r') as f:
            data_dict = json.load(f)

        return data_dict
