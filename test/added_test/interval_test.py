from meteor_reasoner.classes import Interval

interval1 = Interval(4, 6, True, True)
interval2 = Interval(5, 6, False, False)
results = Interval.diff(interval1, [interval2])
print([str(res) for res in results])