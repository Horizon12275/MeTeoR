import logging
from meteor_reasoner.classes.interval import *
from meteor_reasoner.classes.literal import *
from collections import defaultdict
import traceback

def get_binary_literals_from_rule(rule):
    """
    Get all binary literals from a rule.
    Args:
        rule (Rule instance):
    Returns:
        binary_literals (a list of BinaryLiteral instances):
    """
    binary_literals = []
    for literal in rule.body:
        if isinstance(literal, BinaryLiteral):
            binary_literals.append(literal)
    return binary_literals

def get_binary_literals_from_program(program):
    """
    Get all binary literals from a program.
    Args:
        program (Program instance):
    Returns:
        binary_literals (a list of BinaryLiteral instances):
    """
    binary_literals = []
    for rule in program:
        binary_literals.extend(get_binary_literals_from_rule(rule))
    return binary_literals

def create_binary_literal_dict_pair(program):
    """
    Create a dictionary object with binary literals as keys and a list of literals as values.
    Args:
        program (Program instance):
    Returns:
        binary_literal_dict_pair (a dictionary object):
    """
    binary_literals = get_binary_literals_from_program(program)
    binary_literal_dict_pair = defaultdict(list)
    for binary_literal in binary_literals:
        left_literal_predicate = binary_literal.left_literal.get_predicate()
        right_literal_predicate = binary_literal.right_literal.get_predicate()
        binary_literal_dict_pair[left_literal_predicate].append(right_literal_predicate)
        binary_literal_dict_pair[right_literal_predicate].append(left_literal_predicate)
    return binary_literal_dict_pair