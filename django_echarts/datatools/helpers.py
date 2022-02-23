"""
数据处理函数
See more detail https://mp.weixin.qq.com/s/ZYU7g3mVF-cvRZ3JyMIngw
"""


def adjust_max_min(values: list):
    """保持折线上下高度占据 Y 轴范围的三分之二。 1/6,1/3,1/3,1/6"""
    ma = max(values)
    mi = min(values)
    nmax = int(ma + (ma - mi) / 2) + 1
    nmin = int(mi - (ma - mi) / 2)
    return nmax, nmin


def ceil_n(val, n=3):
    return (val // (10 ** n) + 1) * 10 ** n


def floor_n(val, n=3):
    return (val // (10 ** n)) * 10 ** n


def concat_if(val: str, fix: str, o=None):
    """
    concat_if('xxx','+.html')
    """
    pass
