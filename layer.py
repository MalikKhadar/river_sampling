from scipy import stats
import numpy as np
from datetime import datetime

class Span:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def contains(self, val):
        if val >= self.min and val < self.max:
            return True
        return False

class Filter:
    def __intit__(self):
        pass
    def test(row):
        pass

tier = ["year", "season", "month", "weekday", "time", "custom dt"]

class Time_Filter(Filter):
    def __init__(self, tier, span):
        self.tier = tier
        self.span = span
    
    def test(self, row):
        dt = datetime.fromisoformat(row[0])
        if self.tier == "year":
            return self.span.contains(dt.year)
        elif self.tier == "month":
            return self.span.contains(dt.month)
        elif self.tier == "weekday":
            return self.span.contains(dt.day)
        elif self.tier == "hour":
            return self.span.contains(dt.time().hour)
        elif self.tier == "minute":
            return self.span.contains(dt.time().minute)
        elif self.tier == "specific":
            return self.span.contains(dt)

class Val_Filter(Filter):
    def __init__(self, col, span):
        self.col = col
        self.span = span

    def test(self, row):
        return self.span.contains(row[self.col])

class Perc_Filter(Filter):
    def __init__(self, col, span, data):
        self.col = col
        self.span = span
        self.data = np.array(data[1:])

    def test(self, row):
        perc = stats.percentileofscore(self.data[:,self.col], row[self.col])
        return self.span.contains(perc)

class Layer:
    def __init__(self, filters):
        self.filters = filters

    def apply(self, data):
        filtered = []
        for row in data[1:]:
            keep = True
            for filter in self.filters:
                if not filter.test(row):
                    keep = False
                    break
            if keep == True:
                filtered.append(row)
        return filtered

d = [["day", "temp", "speed"], ["1990-10-01T01:15:00.000-04:00",2,3], ["2012-03-07T00:00:00.000-05:00",5,6], ["2013-06-21T23:30:00.000-04:00",8,9]]
#v1 = Val_Filter(1, Span(3, 10))
#v2 = Val_Filter(2, Span(5, 11))
#p1 = Perc_Filter(0, Span(25, 75), d)
t1 = Time_Filter("year", Span(1990, 2013))
l = Layer([t1])
print(l.apply(d))