import logging
from meteor_reasoner.classes.interval import *
from collections import defaultdict
import traceback

def get_min_max_rational(D):
    min_val = float("inf")
    max_val = float("-inf")
    for predicate in D:
        for entity in D[predicate]:
            for intv in D[predicate][entity]:
                min_val = min(min_val, intv.left_value)
                max_val = max(max_val, intv.right_value)
    return min_val, max_val

def print_dataset_with_entity_name(D, entity_name):
    """
    Print all facts in D with the specified entity name.
    Args:
        D (a dictionary object):
        entity_name (str): The name of the entity.
    """
    for predicate in D:
        for entity, intervals in D[predicate].items():
            if ",".join([item.name for item in entity]) == entity_name:
                for interval in intervals:
                    print(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval))

def dataset_is_empty(D):
    """
    Check if the dataset is empty.
    Args:
        D (a dictionary object):

    Returns:
        bool: True if the dataset is empty, False otherwise.
    """
    for predicate in D:
        for entity, intervals in D[predicate].items():
            for interval in intervals:
                if len(entity) == 1 and entity[0].name == "nan":
                     #print("Dataset is not empty")
                     return False
                else:
                    #print("Dataset is not empty")
                    return False
    return True

def print_dataset(D):
    """
    Print all facts in D, the outputing form
    Args:
        D (a dictionary object):

    Returns:

    """
    for predicate in D:
        for entity, intervals in D[predicate].items():
            for interval in intervals:
                if len(entity) == 1 and entity[0].name == "nan":
                     print(predicate+"@"+str(interval))
                else:
                    print(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval))


def save_dataset_to_file(filename, D):
    """
       Print all facts in D, the outputing form
       Args:
           D (a dictionary object):

       Returns:

       """
    filewriter = open(filename, "w")
    for predicate in D:
        for entity, intervals in D[predicate].items():
            for interval in intervals:
                if len(entity) == 1 and entity[0].name == "nan":
                    filewriter.write(predicate + "@" + str(interval)+"\n")
                else:
                    filewriter.write(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval)+"\n")

def return_dataset(D):
    """
    Print all facts in D, the outputing form
    Args:
        D (a dictionary object):

    Returns:

    """
    res = ""
    for predicate in D:
        if "TMP" in predicate:
            continue
        if type(D[predicate]) == list:
            for interval in D[predicate]:
                res += predicate+"@"+str(interval) +"<br/>"
        else:
            for entity, intervals in D[predicate].items():
                entity_name = ",".join([item.name for item in entity if item.name != "nan"])
                for interval in intervals:
                    if entity_name != "":
                       res += predicate+"("+ entity_name + ")@"+str(interval) + "<br/>"
                    else:
                        res += predicate + "@" + str(interval) + "<br/>"

    return res


def yield_dataset(D):
    """
    Print all facts in D, the outputing form
    Args:
        D (a dictionary object):

    Returns:

    """
    res = ""
    for predicate in D:
        if "TMP" in predicate:
            continue
        if type(D[predicate]) == list:
            for interval in D[predicate]:
                res += predicate+"@"+str(interval) +"<br/>"
        else:
            for entity, intervals in D[predicate].items():
                entity_name = ",".join([item.name for item in entity if item.name != "nan"])
                for interval in intervals:
                    if entity_name != "":
                       yield predicate+"("+ entity_name + ")@"+str(interval)
                    else:
                        yield predicate + "@" + str(interval)

    return res



def print_predicate(predicate, D, num=100000):
    """
    Print all fact with a specified predicate.
    Args:
        predicate (str):
        D (a dictionary object):

    Returns:

    """
    if predicate in D:
        cnt = 0
        if type(D[predicate]) == list:
            for interval in D[predicate]:
                cnt += 1
                logging.info(predicate + "@" + str(interval))
                if cnt > num:
                    break
        else:
            for entity, intervals in D[predicate].items():
                for interval in intervals:
                    cnt += 1
                    if cnt < num:
                        logging.info(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval))

        logging.info("The total number of the predicate({}) is {}".format(predicate, cnt))

    else:
        print("{} does not exist in D!".format(predicate))


def save_predicate(predicate, D, outfilename="result.txt"):
    """
    Print all fact with a specified predicate.
    Args:
        predicate (str):
        D (a dictionary object):

    Returns:

    """
    with open(outfilename, "w") as file:
        if predicate in D:
            if type(D[predicate]) == list:
                for interval in D[predicate]:
                    file.write(predicate + "@" + str(interval))
                    file.write("\n")
            else:
                for entity, intervals in D[predicate].items():
                    for interval in intervals:
                        file.write(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval))
                        file.write("\n")
        else:
            print("{} does not exist in D!".format(predicate))


def save_dataset(D, outfilename):
    with open(outfilename, "w") as file:
        for predicate in D:
            if type(D[predicate]) == list:
                for interval in D[predicate]:
                    file.write(predicate + "@" + str(interval))
                    file.write("\n")
            else:
                for entity, intervals in D[predicate].items():
                    for interval in intervals:
                        file.write(predicate + "(" + ",".join([item.name for item in entity]) + ")@" + str(interval))
                        file.write("\n")

def dataset_intersection(D1, D2):
    """
    Compute the intersection of two datasets.
    Args:
        D1 (dict): The first dataset where each D1[predicate][entity] is a list of Interval instances.
        D2 (dict): The second dataset where each D2[predicate][entity] is a list of Interval instances.

    Returns:
        dict: A new dataset with the intersection of intervals.
    """
    result = defaultdict(lambda: defaultdict(list))
    for predicate in D1:
        if predicate in D2:
            result[predicate] = {}
            for entity in D1[predicate]:
                if entity in D2[predicate]:
                    result[predicate][entity] = Interval.list_intersection(D1[predicate][entity], D2[predicate][entity])
    return result

def dataset_union(D1, D2):
    """
    Compute the union of two datasets
    Args:
        D1 (a dictionary object):
        D2 (a dictionary object):

    Returns:
        D (a dictionary object): the union of D1 and D2
    """
    D = defaultdict(lambda: defaultdict(list))
    for predicate in set(D1.keys()).union(D2.keys()):
        D[predicate] = {}
        entities = set(D1.get(predicate, {}).keys()).union(D2.get(predicate, {}).keys())
        for entity in entities:
            intervals1 = D1.get(predicate, {}).get(entity, [])
            intervals2 = D2.get(predicate, {}).get(entity, [])
            D[predicate][entity] = Interval.list_union(intervals1, intervals2)
    return D

def dataset_union_inplace(D1, D2):
    """
    Compute the union of two datasets by modifying D1 in-place
    Args:
        D1 (a dictionary object): will be modified in-place
        D2 (a dictionary object): will be read but not modified
    """
    for predicate in D2.keys():
        if predicate not in D1:
            D1[predicate] = {}
        for entity in D2[predicate].keys():
            if entity not in D1[predicate]:
                D1[predicate][entity] = []
            intervals1 = D1[predicate][entity]
            intervals2 = D2[predicate][entity]
            D1[predicate][entity] = Interval.list_union(intervals1, intervals2)
    return D1  # Return D1 for chaining, though it's modified in-place

def dataset_union_opt(D_large, D_small):
    D = defaultdict(lambda: defaultdict(list))
    # 先处理小数据集
    for predicate in D_small:
        for entity in D_small[predicate]:
            if entity in D_large.get(predicate, {}):
                D[predicate][entity] = Interval.list_union(
                    D_large[predicate][entity], D_small[predicate][entity]
                )
            else:
                D[predicate][entity] = D_small[predicate][entity]
    
    # 再处理大数据集独有的部分
    for predicate in D_large:
        if predicate not in D_small:
            D[predicate] = D_large[predicate]
        else:
            for entity in D_large[predicate]:
                if entity not in D_small[predicate]:
                    D[predicate][entity] = D_large[predicate][entity]
    return D

def dataset_difference(D1, D2):
    """
    Compute the difference of two datasets
    Args:
        D1 (a dictionary object):
        D2 (a dictionary object):

    Returns:
        D (a dictionary object): the difference of D1 and D2, i.e., D1 - D2
    """
    D = defaultdict(lambda: defaultdict(list))
    for predicate in D1:
        if predicate in D2:
            D[predicate] = {}
            for entity in D1[predicate]:
                if entity in D2[predicate]:
                    D[predicate][entity] = Interval.diff_list_incre(D1[predicate][entity], D2[predicate][entity])
                else:
                    D[predicate][entity] = D1[predicate][entity]
        else:
            D[predicate] = D1[predicate]
    return D

def dataset_difference_opt(D1, D2):
    """
    Compute the difference of two datasets
    Args:
        D1 (a dictionary object):
        D2 (a dictionary object):

    Returns:
        D (a dictionary object): the difference of D1 and D2, i.e., D1 - D2
    """
    D = defaultdict(lambda: defaultdict(list))
    for predicate in D1:
        if predicate in D2:
            D[predicate] = {}
            for entity in D1[predicate]:
                if entity in D2[predicate]:
                    D[predicate][entity] = Interval.diff_list_incre_opt(D1[predicate][entity], D2[predicate][entity])
                else:
                    D[predicate][entity] = D1[predicate][entity]
        else:
            D[predicate] = D1[predicate]
    return D

def dataset_difference_inplace(D1, D2):
    """
    Compute the difference of two datasets by modifying D1 in-place, optimized for cases where D1 >> D2
    Args:
        D1 (a dictionary object): Will be modified in-place (assumed to be much larger than D2)
        D2 (a dictionary object): The dataset to subtract from D1
    """
    for predicate in D2:
        if predicate in D1:
            for entity in D2[predicate]:
                if entity in D1[predicate]:
                    # Compute the difference and update in-place
                    diff_intervals = Interval.diff_list_incre_opt(D1[predicate][entity], D2[predicate][entity])
                    if diff_intervals:  # Only keep if there are remaining intervals
                        D1[predicate][entity] = diff_intervals
                    else:  # Remove entity if no intervals left
                        del D1[predicate][entity]
            
            # Remove predicate if it's now empty
            if not D1[predicate]:
                del D1[predicate]
    # Predicates in D1 that aren't in D2 remain unchanged

def dataset_Same(D1, D2):
    """
    Check if two datasets are the same.
    Args:
        D1 (a dictionary object):
        D2 (a dictionary object):

    Returns:
        bool: True if D1 and D2 are the same, False otherwise.
    """
    try:
        for predicate in D1:
            for entity in D1[predicate]:
                for i in range(len(D1[predicate][entity])):
                    if D1[predicate][entity][i] != D2[predicate][entity][i]:
                        print("The interval {} is not the same".format(D1[predicate][entity][i]))
                        return False
            for entity in D2[predicate]:
                for i in range(len(D2[predicate][entity])):
                    if D2[predicate][entity][i] != D1[predicate][entity][i]:
                        print("The interval {} is not the same".format(D2[predicate][entity][i]))
                        return False
    except Exception as e:
        print("The error is in the dataset_Same")
        print(f"Exception: {e}")
        # traceback.print_exc()
        return False
    return True

def count_facts(D):
    """
    Count the number of facts in the dataset D.
    Args:
        D (a dictionary object): The dataset where each D[predicate][entity] is a list of Interval instances.

    Returns:
        int: The total number of facts in the dataset.
    """
    count = 0
    for predicate in D:
        if type(D[predicate]) == list:
            count += len(D[predicate])
        else:
            for entity, intervals in D[predicate].items():
                count += len(intervals)
    return count