import re

import calendar
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


class Visualizer:
    def __init__(self, data: dict):
        self.data = data
        self.days = list(map(lambda d: re.split(r'\d{4}-\d{2}-', d)[-1], data.keys()))
        self.moths = map(lambda d: re.search(r'-(\d{2})-', d).group(1), data.keys())
        self.years = map(lambda d: re.split(r'\d{4}-', d)[0], data.keys())

    def tasks_plot(self, mode='date', trend_line=''):
        plt.rcParams["figure.figsize"] = (20, 10)

        if mode == 'date':
            num_of_tasks = list(map(lambda v: len(v), self.data.values()))
            scale_factor = 3

            tasks_spline = interp1d(np.linspace(0, len(self.days), num=len(self.days), endpoint=True),
                                    num_of_tasks, kind='cubic')
            new_x_axis = np.linspace(0, len(self.days), num=(scale_factor * len(self.days)), endpoint=True)
            tasks_spline = tasks_spline(new_x_axis)

            fig1, ax1 = plt.subplots(1)
            ax1.plot(tasks_spline)
            ax1.set_yticks(np.arange(0, tasks_spline.max() + 1, 1.))
            ax1.set_xticks(np.arange(new_x_axis.min(), scale_factor * new_x_axis.max(), scale_factor))
            ax1.set_xticklabels(self.days)
            ax1.tick_params(axis='x', which='major', labelsize=15)

            if len(self.days) > 31:
                ax1.set_xticks([])  # disable the first axis to avoid labels overlap

            ax2 = ax1.twiny()  # make a second axis (month axis)
            ax2.spines["bottom"].set_position(("axes", -0.10))
            ax2.tick_params('both', length=0, width=0, which='minor', labelsize=15)
            ax2.tick_params('both', direction='in', which='major')
            ax2.xaxis.set_ticks_position("bottom")
            ax2.xaxis.set_label_position("bottom")

            # todo support several (> 2) month labels
            month_labels = self.prepare_month_labels()
            ax2.set_xticks(np.arange(0, len(month_labels), 1))
            ax2.xaxis.set_major_formatter(ticker.NullFormatter())
            ax2.xaxis.set_minor_locator(ticker.FixedLocator([np.arange(0, len(month_labels), 1)]))
            ax2.xaxis.set_minor_formatter(ticker.FixedFormatter(month_labels))

            fig1.show()

    def prepare_month_labels(self):
        month_numbers = sorted(set(self.moths))
        return list(map(lambda n: calendar.month_name[int(n)], month_numbers))

    def hist(self):
        ...
