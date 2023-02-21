"""
数据处理函数
See more detail https://mp.weixin.qq.com/s/ZYU7g3mVF-cvRZ3JyMIngw
"""
import statistics
from collections import namedtuple, UserList
from dataclasses import dataclass
from typing import List, Tuple


def adjust_max_min(values: list):
    ma = max(values)
    mi = min(values)
    nmax = int(ma + (ma - mi) / 2) + 1
    nmin = int(mi - (ma - mi) / 2)
    return nmax, nmin


def ceil_n(val, n=3):
    return (val // (10 ** n) + 1) * 10 ** n


def floor_n(val, n=3):
    return (val // (10 ** n)) * 10 ** n


QuartilesRank = namedtuple('QuartilesRank', 'rank text color')


@dataclass
class SeriesStatisticsValue:
    """一维数据统计值"""
    label: str
    index: int
    num: int
    avg: int
    std_deviation: int
    min_: int
    q1: int
    q2: int
    q3: int
    max_: int

    @property
    def boxplot_values(self) -> Tuple:
        """Return five values for boxplot"""
        return (self.min_, self.q1, self.q2, self.q3, self.max_)

    def evaluate(self, value: int) -> QuartilesRank:
        if value < self.q1:
            return QuartilesRank(rank=1, text='下', color='danger')
        elif value < self.q2:
            return QuartilesRank(rank=2, text='中下', color='warning')
        elif value < self.q3:
            return QuartilesRank(rank=2, text='中上', color='info')
        else:
            return QuartilesRank(rank=2, text='上', color='success')

    @classmethod
    def from_(cls, data: List, label: str = '', index=0):
        q1, q2, q3 = list(map(int, statistics.quantiles(data)))
        return cls(label=label, num=len(data),
                   avg=int(statistics.mean(data)), std_deviation=int(statistics.pstdev(data)),
                   min_=min(data), max_=max(data), q1=q1, q2=q2, q3=q3, index=index)


class SeriesStatisticsList(UserList[SeriesStatisticsValue]):

    @property
    def axis_values(self):
        return [item.label for item in self]

    @property
    def boxplot_data(self):
        return [list(item.boxplot_values) for item in self]
