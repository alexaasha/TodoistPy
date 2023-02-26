import os
import json


class TodoistCacheManager:
    events_dict = None

    def __init__(self, path_to_cache: str):
        self.path_to_cache = path_to_cache
        self.__cache_existence_flag = True if os.path.exists(path_to_cache) else False

    def is_cache_exists(self):
        return self.__cache_existence_flag

    # todo consider making this deprecated
    def get_last_date(self) -> str:
        events_dict = self.read() if self.events_dict is None else self.events_dict
        return list(events_dict.keys())[-1]

    def write(self, data_dict: dict):
        with open(self.path_to_cache, 'w') as f:
            json.dump(data_dict, f, indent='  ')

    def remove_cache(self):
        if self.__cache_existence_flag:
            os.remove(self.path_to_cache)

    def read(self) -> dict:
        with open(self.path_to_cache, 'r') as f:
            self.events_dict = json.load(f)

        return self.events_dict
