from enum import Enum


class ModeType(Enum):
    DATE = 1
    TIME = 2


class Visualizer:
    def __init__(self, data):
        self.x, self.y = data

    def __aggregate(self, mode=ModeType.DATE):
        if mode == ModeType.DATE:
            return list(map(lambda dt: dt.split('T')[0], self.x))

        if mode == ModeType.TIME:
            return list(map(lambda dt: dt.split('T')[1], self.x))

    def plot(self, mode='date', trend_line=''):
        ...

    def hist(self):
        ...
