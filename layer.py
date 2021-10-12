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
    def test(self, row):
        pass
    def print(self):
        pass

tier = {
    "Year": 0,
    "Season": 4,
    "Month": 12,
    "Day of week": 7,
    "Hour": 24,
    "Minute": 60,
    "Specific DateTime": 0
}

class Time_Filter(Filter):
    def __init__(self, tier, span):
        self.tier = tier
        self.span = span
    
    def test(self, row):
        dt = datetime.fromisoformat(row[0])
        if self.tier == "Year":
            return self.span.contains(dt.year)
        elif self.tier == "Month":
            return self.span.contains(dt.month)
        elif self.tier == "Day of week":
            return self.span.contains(dt.day)
        elif self.tier == "Hour":
            return self.span.contains(dt.time().hour)
        elif self.tier == "Minute":
            return self.span.contains(dt.time().minute)
        elif self.tier == "Specific DateTime":
            return self.span.contains(dt)
        
    def print(self):
        p = "Time:\t"
        p += self.tier + " "
        p += str(self.span.min)
        p += " <= date < "
        p += self.tier + " "
        p += str(self.span.max)
        print(p)

class Val_Filter(Filter):
    def __init__(self, col, span):
        self.col = col
        self.span = span

    def test(self, row):
        return self.span.contains(row[self.col])

    def print(self):
        p = "Value:\t"
        p += str(self.span.min) + " <= "
        p += self.col + " < "
        p += str(self.span.max)
        print(p)

class Perc_Filter(Filter):
    def __init__(self, col, span, data):
        self.col = col
        self.span = span
        self.data = np.array(data[1:])

    def test(self, row):
        perc = stats.percentileofscore(self.data[:,self.col], row[self.col])
        return self.span.contains(perc)

    def print(self):
        p = "Percentile:\t"
        p += str(self.span.min) + "th <= "
        p += self.col + " < "
        p += str(self.span.max) + "th"
        print(p)

class Layer:
    def __init__(self, filters=[]):
        self.filters = filters

    def add_filter(self, filter):
        self.filters.append(filter)

    def apply(self, data):
        filtered = []
        for row in data[1:]:
            for filter in self.filters:
                if filter.test(row) == True:
                    filtered.append(row)
                    break
        return filtered

    def print(self):
        for filter in self.filters:
            filter.print()

class Strategy:
    def __init__(self, layers=[Layer()]):
        self.layers = layers

    def add_layer(self, layer):
        self.layers.append(layer)

    def apply(self, data):
        for layer in self.layers:
            data = layer.apply(data)

    def print(self):
        for l in range(len(self.layers)):
            print("\tLayer " + str(l))
            self.layers[l].print()

'''
d = [["day", "temp", "speed"], ["1990-10-01T01:15:00.000-04:00",2,3], ["2012-03-07T00:00:00.000-05:00",5,6], ["2013-06-21T23:30:00.000-04:00",8,9]]
#v1 = Val_Filter(1, Span(3, 10))
#v2 = Val_Filter(2, Span(5, 11))
#p1 = Perc_Filter(0, Span(25, 75), d)
t1 = Time_Filter("year", Span(1990, 2013))
l = Layer([t1])
print(l.apply(d))'''