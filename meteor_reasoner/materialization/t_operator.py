from meteor_reasoner.materialization.seminaive_join import *
from meteor_reasoner.materialization.naive_join import *
from collections import defaultdict
from meteor_reasoner.classes.interval import *
from meteor_reasoner.utils.operate_dataset import *
from meteor_reasoner.utils.operate_program import *

def naive_immediate_consequence_operator(rules, D, D_index):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        naive_join(rule, D, delta_new, D_index)
    return delta_new


def seminaive_immediate_consequence_operator(rules, D, D_index, delta_old=None):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        seminaive_join(rule, D, delta_old, delta_new, D_index=D_index)
    coalescing_d(delta_new)
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
                        if Interval.intersection(interval, old_interval) is not None:
                            # print interval and old_interval
                            # print("\ninterval: ", interval)
                            # print("old_interval: ", old_interval)
                            new_delta_old[predicate][entity].append(Interval(old_interval.left_value, old_interval.right_value, old_interval.left_open, old_interval.right_open))
                            # print all the intervals in new_delta_old
                            # for interval in new_delta_old[predicate][entity]:
                            #     print("new_delta_old: ", interval)
                            break
                    RuntimeError("The fact in delta_old is not in D")
                else:
                    RuntimeError("The fact in delta_old is not in D")
    # binary_literal_dict_pair = create_binary_literal_dict_pair(rules)
    #print("\nThe binary_literal_dict_pair is: ", binary_literal_dict_pair)
    # if I is not None, check all binary literal pair in rules, if one predicate in the pair is in delta_old
    # then add all the corresponding facts with another predicate in the pair in I to delta_old
    # if I is not None:
    #     for predicate in binary_literal_dict_pair:
    #         if predicate in delta_old:
    #             # add all the fact with the other predicate in the pair in I to delta_old
    #             for another_binary_literal in binary_literal_dict_pair[predicate]:
    #                 if another_binary_literal in I:
    #                     print("\nThe another_binary_literal is: ", another_binary_literal)
    #                     for entity in I[another_binary_literal]:
    #                         print("\nThe entity is: ", entity)
    #                         for interval in I[another_binary_literal][entity]:
    #                             new_delta_old[another_binary_literal][entity].append(Interval(interval.left_value, interval.right_value, interval.left_open, interval.right_open))

    # coalescing_d(new_delta_old)
    # print("\nThe new Delta_D is: ")
    # print_dataset(new_delta_old)
    # print("\nThe new I_minus_D is: ")
    # print_dataset(D)

    # D_index = build_index(D)

    return seminaive_immediate_consequence_operator(rules, D, D_index, new_delta_old)