import json
from typing import List, Dict

import requests

from cache.TodoistCacheManager import TodoistCacheManager
from cache.cacheable import cacheable
from enums.ResourceType import ResourceType


class TodoistConnector:
    todoist_path = 'https://api.todoist.com/sync/v9/'
    cache_manager = TodoistCacheManager('cache.json')

    def __init__(self, path_to_config: str):
        with open(path_to_config, 'r') as json_file:
            self.auth_data = json.load(json_file)
            self.token = f'Bearer {self.auth_data["token"]}'
            self.sync_token = self.auth_data["sync_token"]
            self.mfa_token = self.auth_data["mfa_token"]
            self.session = requests.Session()

    def sync(self, resource_types: List[ResourceType]):
        """
        This method is used for synchronization with todoist api. It yields data of corresponding
        resourceType that wasn't competed.

        :type resource_types: List of resource types to retrieve from API
        """
        resource_string = json.dumps(list(map(lambda rt: rt.value, resource_types)))
        headers = {"Authorization": self.token}
        data = {'sync_token': self.sync_token,
                'resource_types': resource_string,
                'mfa_token': self.mfa_token}
        r = self.session.get(self.todoist_path + 'sync', params=data, headers=headers)
        r = json.loads(r.text)
        self.sync_token = r["sync_token"] if r["sync_token"] != "*" else self.sync_token

        return r

    @cacheable(cache_manager=cache_manager)
    def get_completed_items(self, project_id="", limit=30, until="2021-5-29T10:13:00",
                            since="2021-4-29T10:15:00", annotate_notes=False) -> List[Dict]:
        headers = {"Authorization": self.token}
        data = {'limit': limit,
                'until': until,
                'since': since,
                'annotate_notes': annotate_notes
                }
        if project_id != "":
            data.update({'project_id': project_id})

        r = self.session.get(self.todoist_path + 'completed/get_all', params=data, headers=headers)
        return json.loads(r.text)["items"]


if __name__ == '__main__':
    tC = TodoistConnector("../context.json")
    # print(tC.sync([ResourceType.ITEMS]))
    print(tC.get_completed_items())
