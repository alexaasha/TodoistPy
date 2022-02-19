from collections import Counter


class Aggregator:
    def __init__(self, events: list):
        self.events = events

    def perform_aggregation(self, rule='date') -> list:
        """
        Performs an aggregation according to the rule
        :param rule: denotes aggregation according to the part of an event information
        can be 'date' or 'time'
        """
        event_dates = map(lambda e: e['event_date'].rstrip('Z').split('T'), self.events)
        if rule == 'date':
            events_dict = Counter(map(lambda e: e[0], event_dates))
        elif rule == 'time':
            events_dict = Counter(map(lambda e: e[1], event_dates))
        else:
            raise ValueError(f'Invalid rule: {rule}')

        return sorted(events_dict.items(), key=lambda event: event[0])


if __name__ == '__main__':
    events = [{'event_date': '2022-02-19T17:05:16Z'}, {'event_date': '2022-02-19T18:05:16Z'},
              {'event_date': '2022-02-19T19:05:16Z'}, {'event_date': '2022-02-19T20:05:16Z'},
              {'event_date': '2022-02-18T17:05:16Z'}, {'event_date': '2022-02-20T17:05:16Z'}]

    event_fabric = Aggregator(events)
    events_list = event_fabric.perform_aggregation()
    print(events_list)
