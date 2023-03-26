from collections import Counter
from datetime import datetime as time
from typing import List, Dict

from matplotlib import pyplot as plt

from connection.TodoistConnector import TodoistConnector


class Visualizer:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.timestamps = list(
            map(
                # 'Z' symbol at the end of the timestring is redundant
                lambda d: time.fromisoformat(d["completed_at"][:-1]),
                data
            )
        )

    def tasks_plot(self, mode='date', trend_line=''):
        if mode == 'date':
            date_list = [timestamp.date() for timestamp in self.timestamps]
            dates_counter = Counter(date_list)

            plt.plot(list(dates_counter.keys()), list(dates_counter.values()))
            plt.show()

    def hist(self):
        ...

    def main(self):
        date_list = [timestamp.date() for timestamp in self.timestamps]
        dates_counter = Counter(date_list)
        data = {ts.year: {m.month: {day_count[0].day: day_count[1] for day_count in sorted(dates_counter.items()) if
                                    day_count[0].month == m.month and day_count[0].year == ts.year} for m in
                          sorted(dates_counter.keys()) if m.year == ts.year} for ts in sorted(dates_counter.keys())}

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        label_group_bar(ax, data)
        fig.subplots_adjust(bottom=0.3)
        fig.savefig('label_group_bar_example.png')

# todo refactor code below
def mk_groups(data):
    try:
        newdata = data.items()
    except:
        return

    thisgroup = []
    groups = []
    for key, value in newdata:
        newgroups = mk_groups(value)
        if newgroups is None:
            thisgroup.append((key, value))
        else:
            thisgroup.append((key, len(newgroups[-1])))
            if groups:
                groups = [g + n for n, g in zip(newgroups, groups)]
            else:
                groups = newgroups
    return [thisgroup] + groups


def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                      transform=ax.transAxes, color='black')
    line.set_clip_on(False)
    ax.add_line(line)


def label_group_bar(ax, data):
    groups = mk_groups(data)
    xy = groups.pop()
    x, y = zip(*xy)
    ly = len(y)
    xticks = range(1, ly + 1)

    ax.bar(xticks, y, align='center')
    ax.set_xticks(xticks)
    ax.set_xticklabels(x)
    ax.set_xlim(.5, ly + .5)
    ax.yaxis.grid(True)

    scale = 1. / ly
    for pos in range(ly + 1):  # change xrange to range for python3
        add_line(ax, pos * scale, -.1)
    ypos = -.2
    while groups:
        group = groups.pop()
        pos = 0
        for label, rpos in group:
            lxpos = (pos + .5 * rpos) * scale
            ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes)
            add_line(ax, pos * scale, ypos)
            pos += rpos
        add_line(ax, pos * scale, ypos)
        ypos -= .1


if __name__ == "__main__":
    connector = TodoistConnector("../context.json")

    items = connector.get_completed_items(since="2023-1-01T00:00:00", until="2023-1-29T00:00:00", limit=200)
    vis = Visualizer(items)
    print(items)
    vis.main()
