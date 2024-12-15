from meteor_reasoner.materialization.seminaive_join import *
from meteor_reasoner.materialization.naive_join import *
from collections import defaultdict
from meteor_reasoner.classes.interval import *

def naive_immediate_consequence_operator(rules, D, D_index):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        naive_join(rule, D, delta_new, D_index)
    return delta_new


def seminaive_immediate_consequence_operator(rules, D, D_index, delta_old=None):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        seminaive_join(rule, D, delta_old, delta_new, D_index=D_index)

    return delta_new

def incre_seminaive_immediate_consequence_operator(rules, D, D_index, delta_old=None):
    # We need to fill the corresponding part in delta old according to the fact in D
    # Traverse the fact in delta_old, if the fact can be found in D, then add the rest of the complete interval to delta_old
    new_delta_old = defaultdict(lambda: defaultdict(list))
    for predicate in delta_old:
        for entity in delta_old[predicate]:
            for interval in delta_old[predicate][entity]:
                if entity in D[predicate]:
                    for old_interval in D[predicate][entity]:
                        if Interval.inclusion(interval, old_interval):
                            new_delta_old[predicate][entity].append(Interval(old_interval.left_value, old_interval.right_value, old_interval.left_open, old_interval.right_open))
                            break
                    RuntimeError("The fact in delta_old is not in D")
                else:
                    RuntimeError("The fact in delta_old is not in D")
    return seminaive_immediate_consequence_operator(rules, D, D_index, new_delta_old)