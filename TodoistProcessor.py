from collections import Counter
from datetime import datetime as dt
import matplotlib.pyplot as plt

from TodoistCacheManager import TodoistCacheManager
from TodoistConnector import TodoistConnector
from Visualizer import Visualizer
from enums import ModeType


class TodoistProcessor(TodoistConnector):
    def __init__(self, path_to_config: str):
        super().__init__(path_to_config)
        self.cacheManager = TodoistCacheManager('cache.csv')
        self.time_pattern = '%Y-%m-%dT%H:%M:%SZ'

    def get_project_info(self, project_name: str):
        try:
            filtered_list = filter(lambda p: p['name'] == project_name, self.api.state['projects'])
            return self.api.projects.get(next(filtered_list)['id'])
        except StopIteration:
            return 'no such project'

    def get_events(self, event_type='completed', time_range=('-', '-')):
        """
        This code retrieves and count all tasks with event_type per each week.
        Note that the maximum tasks per week should be no more than 100.
        If you need receive more tasks use offset option in self.api.activity.get().
        :param time_range: tuple of strings (%Y-%m-%dT%H:%M:%SZ) denoting the beginning
         and end of time interval. If you want to omit beginning or end, just pass "-" string.
        Range is inclusive.
        :param event_type: type of event (see all available options on official site).
        :return: list of tuples where first element is date, second is number of tasks
         of event_type corresponding by that date.
        """

        if not self.cacheManager.is_cache_exists():
            events_list = self.__pull_events_from_api(event_type)
        else:
            self.__pull_events_from_api(event_type, update=True)
            events_list = self.__pull_events_from_cache()

        if len(time_range) == 2:
            beginning, end = time_range
            fmt_beginning = dt.strptime(beginning, self.time_pattern) if beginning != '-' else dt.min
            fmt_end = dt.strptime(end, self.time_pattern) if end != '-' else dt.max
            events_list = list(
                filter(lambda t: fmt_beginning <= dt.strptime(t[0], self.time_pattern) <= fmt_end,
                       events_list)
            )
        else:
            raise ValueError('Invalid time_range')

        return events_list

    def __pull_events_from_api(self, event_type='completed', update=False):
        """
        *except the last day
        :param event_type:
        :param update:
        :return:
        """
        last_date = self.cacheManager.get_last_line().split(',')[0] if update else ''

        count, limit, page = -1, 100, 0
        pulled_data = []
        while True:
            part_of_events = self.api.activity.get(page=page, limit=limit, event_type=event_type)['events']
            if len(part_of_events) == 0:
                break
            events_dict = Counter(map(lambda e: e['event_date'], part_of_events))
            events_list = sorted(events_dict.items(), key=lambda e: e[0])
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

        self.cacheManager.write(map(lambda t: f'{t[0]},{str(t[1])}\n', pulled_data))
        return pulled_data

    def __pull_events_from_cache(self):
        func_to_read = lambda d: (
            map(lambda t: (t[0], int(t[1])),
                map(lambda t: tuple(t.strip('\n').split(',')), d))
        )
        return self.cacheManager.read(func_to_read)

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
    connector = TodoistProcessor('context.json')
    lst = connector.get_events(time_range=("-", "2021-08-01T00:00:00Z"))
    lst = TodoistProcessor.aggregate(lst)
    x, y = tuple(zip(*lst))
    print(len(x))
    print(sum(y) / len(y))
    plt.plot(x, y)
    plt.show()
    # vis = Visualizer(list(lst))
    # vis.plot()
