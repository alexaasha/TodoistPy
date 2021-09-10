import json

from todoist import TodoistAPI


class TodoistConnector:
    def __init__(self, path_to_config: str):
        with open(path_to_config, 'r') as json_file:
            self.auth_data = json.load(json_file)
            self.api = TodoistAPI(self.auth_data['token'])
            self.api.sync()

    def get_list_of_projects(self):
        return self.api.state['projects']
