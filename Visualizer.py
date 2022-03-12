import re
from matplotlib import pyplot as plt


class Visualizer:
    def __init__(self, data: dict):
        self.data = data

    def tasks_plot(self, mode='date', trend_line=''):
        if mode == 'date':
            num_of_tasks = list(map(lambda v: len(v), self.data.values()))
            dates = list(map(lambda d: re.split(r'\d{4}-', d)[-1], self.data.keys()))
            plt.plot(dates, num_of_tasks)
            plt.xticks(rotation=90)
            plt.tick_params(axis='x', which='major', labelsize=5)
            plt.show()

    def hist(self):
        ...
