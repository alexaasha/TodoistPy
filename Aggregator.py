from sortedcontainers import SortedSet


class Aggregator:
    def __init__(self, events: list):
        self.events = events

    def perform_aggregation(self) -> list:
        """
        Performs an aggregation according to the rule
        """
        dates = SortedSet(map(lambda e: e['event_date'].split('T')[0], self.events))
        dates_dict = dict(zip(dates, [[] for _ in range(len(dates))]))

        for event in self.events:
            event_date = event['event_date']
            date, time = event_date.rstrip('Z').split('T')
            dates_dict[date].append(time)

        return list(dates_dict.items())


if __name__ == '__main__':
    event_list = [{'event_date': '2022-02-19T17:05:16Z'}, {'event_date': '2022-02-19T18:05:16Z'},
                  {'event_date': '2022-02-22T18:05:16Z'}, {'event_date': '2022-01-22T18:05:16Z'},
                  {'event_date': '2022-02-19T19:05:16Z'}, {'event_date': '2022-02-19T20:05:16Z'},
                  {'event_date': '2022-02-18T17:05:16Z'}, {'event_date': '2022-02-20T17:05:16Z'}]

    event_fabric = Aggregator(event_list)
    events_list = event_fabric.perform_aggregation()
    print(events_list)
