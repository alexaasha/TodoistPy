from collections import Counter
from datetime import datetime as dt

from Aggregator import Aggregator
from cache.TodoistCacheManager import TodoistCacheManager
from connection.TodoistConnector import TodoistConnector
from enums.ModeType import ModeType
from enums.ResourceType import ResourceType


class TodoistProcessor:
    def __init__(self, path_to_config: str):
        self.connector = TodoistConnector(path_to_config)
        self.cacheManager = TodoistCacheManager('cache.json')
        self.time_pattern = '%Y-%m-%d'

    def get_project_info(self, project_name: str):
        project_info = dict(filter(lambda p: p['name'] == project_name,
                                   self.connector.sync([ResourceType.PROJECTS])['projects']))
        if len(project_info) == 0:
            raise Exception('No such project')
        return project_info

    def get_items(self, time_range=('-', '-')):
        """
        This code retrieves and count all tasks with event_type per each week.
        Note that the maximum tasks per week should be no more than 100.
        If you need receive more tasks use offset option in self.api.activity.get().
        :param time_range: tuple of strings (%Y-%m-%dT%H:%M:%SZ) denoting the beginning
         and end of time interval. If you want to omit beginning or end, just pass "-" string.
        Range is inclusive.
        :return: list of tuples where first element is date, second is number of tasks
         of event_type corresponding by that date.
        """

        items_dict = self.connector.get_completed_items()

        if len(time_range) == 2:
            beginning, end = time_range
            fmt_beginning = dt.strptime(beginning, self.time_pattern) if beginning != '-' else dt.min
            fmt_end = dt.strptime(end, self.time_pattern) if end != '-' else dt.max
            items_dict = dict(
                filter(lambda t: fmt_beginning <= dt.strptime(t[0], self.time_pattern) <= fmt_end,
                       items_dict.items())
            )
        else:
            raise ValueError('Invalid time_range')

        return items_dict

    def __pull_events_from_api(self, event_type='completed', update=False):
        """
        *except the last day
        :param event_type:
        :param update:
        :return:
        """
        last_date = self.cacheManager.get_last_date() if update else ''

        count, limit, page = -1, 100, 0
        pulled_data = []
        while True:
            part_of_events = self.api.activity.sync(page=page, limit=limit, event_type=event_type)['events']
            if len(part_of_events) == 0:
                break

            aggregator = Aggregator(part_of_events)
            events_list = aggregator.perform_aggregation()
            if update:
                events_list = list(
                    filter(lambda t: dt.strptime(last_date, self.time_pattern) < dt.strptime(t[0], self.time_pattern),
                           events_list)
                )

                if len(events_list) == 0:
                    break

            if len(pulled_data) > 0:
                if pulled_data[0][0] == events_list[-1][0]:
                    pulled_data[0] = (pulled_data[0][0], pulled_data[0][1] + events_list[-1][1])
                    pulled_data = events_list[:-1] + pulled_data
                else:
                    pulled_data = events_list + pulled_data
            else:
                pulled_data = events_list[:-1] + pulled_data
            page += 1

        return dict(pulled_data)

    @staticmethod
    def aggregate(data, mode=ModeType.DATE):
        aggr = []
        if mode == ModeType.DATE:
            aggr = list(map(lambda d: d[0].split('T')[0], data))

        if mode == ModeType.TIME:
            aggr = list(map(lambda d: d[0].split('T')[1], data))

        events_dict = Counter(aggr)
        events_list = sorted(events_dict.items(), key=lambda e: e[0])

        return events_list


if __name__ == '__main__':
    processor = TodoistProcessor('context.json')
    received_data = processor.get_items(time_range=("2023-02-26", "-"))
    print(received_data)
