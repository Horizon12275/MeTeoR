from meteor_reasoner.classes.rule import *
from meteor_reasoner.materialization.ground import *
from meteor_reasoner.classes.term import Term
from collections import defaultdict
from meteor_reasoner.materialization.index_build import build_index
from meteor_reasoner.utils.operate_dataset import print_dataset
from meteor_reasoner.materialization.coalesce import coalescing_d
from line_profiler import *

def naive_join(rule, D, delta_new, D_index=None):
    """
    This function implement the join operator when variables exist in the body of the rule.
    Args:
        rule (a Rule instance):
        delta_new (a dictionary object): store new materialized results.
        D (a dictionary object): a global variable storing all facts.
        common_fragment: Canonical Representation related

    Returns:
        None
    """
    head_entity = rule.head.get_entity()
    head_predicate = rule.head.get_predicate()
    literals = rule.body + rule.negative_body
    
    def ground_body(global_literal_index, delta, context):
        if global_literal_index == len(literals):
            T = []
            for i in range(len(rule.body)):
                grounded_literal = copy.deepcopy(literals[i])
                if isinstance(grounded_literal, BinaryLiteral):
                    grounded_literal.set_entity(delta[i])
                else:
                    if grounded_literal.get_predicate() not in ["Bottom", "Top"]:
                        grounded_literal.set_entity(delta[i][0])
                t = apply(grounded_literal, D)
                if len(t) == 0:
                    break
                else:
                    T.append(t)
            n_T = []
            for i in range(len(rule.body), len(literals)):
                grounded_literal = copy.deepcopy(literals[i])
                if isinstance(grounded_literal, BinaryLiteral):
                    grounded_literal.set_entity(delta[i])
                else:
                    if grounded_literal.get_predicate() not in ["Bottom", "Top"]:
                        grounded_literal.set_entity(delta[i][0])

                t = apply(grounded_literal, D)
                if len(t) == 0:
                    break
                else:
                    n_T.append(t)

            if len(n_T) > 0 and len(n_T) == len(rule.negative_body_atoms):
                n_T = interval_merge(T)
            else:
                n_T = []

            try:
                if len(head_entity) > 1 or head_entity[0].name != "nan":
                    replaced_head_entity = []
                    for term in head_entity:
                        if term.type == "constant":
                            replaced_head_entity.append(term)
                        else:
                            if term.name not in context:
                                raise ValueError("Head variables in Rule({}) do not appear in the body".format(str(rule)))
                            else:
                                new_term = Term.new_term(context[term.name])
                                replaced_head_entity.append(new_term)

                    replaced_head_entity = tuple(replaced_head_entity)
                else:
                    replaced_head_entity = head_entity
            except:
                print("hello")

            if len(T) == len(literals):
                T = interval_merge(T)
                exclude_t = []
                if len(T) != 0 and len(n_T) != 0:
                    exclude_t = interval_merge([T, n_T])
                if len(exclude_t) != 0:
                    T = Interval.diff(T, exclude_t)
                if len(T) != 0:
                    if not isinstance(rule.head, Atom):
                        tmp_D = defaultdict(lambda: defaultdict(list))
                        tmp_D[head_predicate][replaced_head_entity] = T
                        tmp_head = copy.deepcopy(rule.head)
                        tmp_head.set_entity(replaced_head_entity)
                        T = reverse_apply(tmp_head, tmp_D)

                    delta_new[head_predicate][replaced_head_entity] += T


        else:
            current_literal = copy.deepcopy(literals[global_literal_index])
            if not isinstance(current_literal, BinaryLiteral):
                if current_literal.get_predicate() in ["Bottom", "Top"]:
                    ground_body(global_literal_index+1, delta, context)
                else:
                    for tmp_entity, tmp_context in ground_generator(current_literal, context, D, D_index):
                        tmp_delata = {global_literal_index: [tmp_entity]}
                        ground_body(global_literal_index+1, {**delta, **tmp_delata}, {**context, **tmp_context})
            else:
                left_predicate = current_literal.left_literal.get_predicate()
                right_predicate = current_literal.right_literal.get_predicate()

                if left_predicate in ["Bottom", "Top"]:
                    for tmp_entity, tmp_context in ground_generator(current_literal.right_literal, context,  D, D_index):
                        tmp_delta = {global_literal_index: [tmp_entity]}
                        ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context})

                elif right_predicate in ["Bottom", "Top"]:
                    for tmp_entity, tmp_context in ground_generator(current_literal.left_literal, context, D, D_index):
                        tmp_delta = {global_literal_index: [tmp_entity]}
                        ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context})

                else:
                    for left_entity, tmp_context1 in ground_generator(current_literal.left_literal, context, D):
                        for right_entity, tmp_context2 in ground_generator(current_literal.right_literal.atom,{**context, **tmp_context1}, D):
                            tmp_delta = {global_literal_index: [left_entity, right_entity]}
                            ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context1, **tmp_context2})

    ground_body(0, {}, dict())

def naive_join_rede(rule, D, I_minus_D, delta_new, D_index=None, I_minus_D_index=None):
    """
    This function implement the join operator when variables exist in the body of the rule.
    Args:
        rule (a Rule instance):
        delta_new (a dictionary object): store new materialized results.
        D (a dictionary object): a global variable storing all facts.
        common_fragment: Canonical Representation related

    Returns:
        None
    """
    head_entity = rule.head.get_entity()
    head_predicate = rule.head.get_predicate()
    head_list = [rule.head]
    literals = head_list + rule.body + rule.negative_body

    def ground_body(global_literal_index, delta, context):
        # Further optimization
        
        if global_literal_index == len(literals):
            T = []
            for i in range(len(rule.body) + 1):
                grounded_literal = copy.deepcopy(literals[i])
                if isinstance(grounded_literal, BinaryLiteral):
                    grounded_literal.set_entity(delta[i])
                else:
                    if grounded_literal.get_predicate() not in ["Bottom", "Top"]:
                        grounded_literal.set_entity(delta[i][0])
                if i == 0:
                    t = apply(grounded_literal, D)
                else:
                    t = apply(grounded_literal, I_minus_D)
                if len(t) == 0:
                    break
                else:
                    T.append(t)
            n_T = []

            try:
                if len(head_entity) > 1 or head_entity[0].name != "nan":
                    replaced_head_entity = []
                    for term in head_entity:
                        if term.type == "constant":
                            replaced_head_entity.append(term)
                        else:
                            if term.name not in context:
                                raise ValueError("Head variables in Rule({}) do not appear in the body".format(str(rule)))
                            else:
                                new_term = Term.new_term(context[term.name])
                                replaced_head_entity.append(new_term)

                    replaced_head_entity = tuple(replaced_head_entity)
                else:
                    replaced_head_entity = head_entity
            except:
                print("hello")

            if len(T) == len(literals):
                T = interval_merge(T)
                exclude_t = []
                if len(T) != 0 and len(n_T) != 0:
                    exclude_t = interval_merge([T, n_T])
                if len(exclude_t) != 0:
                    T = Interval.diff(T, exclude_t)
                if len(T) != 0:
                    if not isinstance(rule.head, Atom):
                        tmp_D = defaultdict(lambda: defaultdict(list))
                        tmp_D[head_predicate][replaced_head_entity] = T
                        tmp_head = copy.deepcopy(rule.head)
                        tmp_head.set_entity(replaced_head_entity)
                        T = reverse_apply(tmp_head, tmp_D)

                    delta_new[head_predicate][replaced_head_entity] += T

        else:
            current_literal = copy.deepcopy(literals[global_literal_index])
            if not isinstance(current_literal, BinaryLiteral):
                if current_literal.get_predicate() in ["Bottom", "Top"]:
                    ground_body(global_literal_index+1, delta, context)
                else:
                    if global_literal_index == 0:
                        for tmp_entity, tmp_context in ground_generator(current_literal, context, D, D_index):
                            tmp_delata = {global_literal_index: [tmp_entity]}
                            ground_body(global_literal_index+1, {**delta, **tmp_delata}, {**context, **tmp_context})
                    else:
                        for tmp_entity, tmp_context in ground_generator(current_literal, context, I_minus_D, I_minus_D_index):
                            tmp_delata = {global_literal_index: [tmp_entity]}
                            ground_body(global_literal_index+1, {**delta, **tmp_delata}, {**context, **tmp_context})
            else:
                left_predicate = current_literal.left_literal.get_predicate()
                right_predicate = current_literal.right_literal.get_predicate()

                if left_predicate in ["Bottom", "Top"]:
                    for tmp_entity, tmp_context in ground_generator(current_literal.right_literal, context,  I_minus_D, I_minus_D_index):
                        tmp_delta = {global_literal_index: [tmp_entity]}
                        ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context})

                elif right_predicate in ["Bottom", "Top"]:
                    for tmp_entity, tmp_context in ground_generator(current_literal.left_literal, context, I_minus_D, I_minus_D_index):
                        tmp_delta = {global_literal_index: [tmp_entity]}
                        ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context})

                else:
                    for left_entity, tmp_context1 in ground_generator(current_literal.left_literal, context, I_minus_D):
                        for right_entity, tmp_context2 in ground_generator(current_literal.right_literal.atom,{**context, **tmp_context1}, I_minus_D):
                            tmp_delta = {global_literal_index: [left_entity, right_entity]}
                            ground_body(global_literal_index + 1, {**delta, **tmp_delta}, {**context, **tmp_context1, **tmp_context2})

    ground_body(0, {}, dict())

def naive_immediate_consequence_operator_rede(rules, D, I_minus_D, D_index=None, I_minus_D_index=None):
    delta_new = defaultdict(lambda: defaultdict(list))
    for i, rule in enumerate(rules):
        naive_join_rede(rule, D, I_minus_D, delta_new, D_index, I_minus_D_index)
    return delta_new

if __name__ == "__main__":

    D = defaultdict(lambda: defaultdict(list))
    D["HeavyWindAffectedState"][tuple([Term("shanghai")])] = [Interval(10, 12, False, False)]

    I_minus_D = defaultdict(lambda: defaultdict(list))
    I_minus_D["HeavyWind"][tuple([Term("pudong")])] = [Interval(10, 11.5, False, False)]
    I_minus_D["LocatedInState"][tuple([Term("pudong"), Term("shanghai")])] = [Interval(10.5, 15, False, False)]

    body = [Literal(Atom("HeavyWind", tuple([Term("Y", "variable")]))),
            Literal(Atom("LocatedInState", tuple([Term("Y", "variable"), Term("X", "variable")])))]
    head = Atom("HeavyWindAffectedState", tuple([Term("X", "variable")]))
    rule = Rule(head, body)

    program = []
    program.append(rule)

    # Build index for D and I_minus_D
    D_index = build_index(D)
    I_minus_D_index = build_index(I_minus_D)

    delta_new = naive_immediate_consequence_operator_rede(program, D, I_minus_D, D_index=D_index, I_minus_D_index=I_minus_D_index)
    print("\nNew materialized results (delta_new):")
    print_dataset(delta_new)

    # for predicate in D:
    #     for rule in program:
    #         if predicate == rule.head.get_predicate():
    #             print("Rule: {}".format(rule))
    #             # replace the entity in the rule with ground entity in rule head and rule body
    #             for entity_list in D[predicate]:
    #                 # create context from entity list and original rule head
    #                 context = {term.name: entity_list[i].name for i, term in enumerate(rule.head.get_entity()) if term.type == "variable"}
    #                 print("Context: {}".format(context))

    #                 # replace the head entity in the rule with the ground entity
    #                 new_rule_head = copy.deepcopy(rule.head)
    #                 if len(new_rule_head.get_entity()) > 1 or new_rule_head.get_entity()[0].name != "nan":
    #                     new_rule_head.set_entity([Term(context.get(term.name, term.name), term.type) for term in new_rule_head.get_entity()])
    #                 else:
    #                     new_rule_head.set_entity([Term("nan")])

    #                 # replace the entity in the body literals according to the context
    #                 new_rule_body = []
    #                 for literal in rule.body:
    #                     new_literal = copy.deepcopy(literal)
    #                     if isinstance(new_literal, BinaryLiteral):
    #                         new_literal.left_literal.set_entity([Term(context.get(term.name, term.name), term.type) for term in new_literal.left_literal.get_entity()])
    #                         new_literal.right_literal.set_entity([Term(context.get(term.name, term.name), term.type) for term in new_literal.right_literal.get_entity()])
    #                     else:
    #                         new_literal.set_entity([Term(context.get(term.name, term.name), term.type) for term in new_literal.get_entity()])
    #                     new_rule_body.append(new_literal)
    #                 new_rule = Rule(new_rule_head, new_rule_body)
    #                 print("New Rule: {}".format(new_rule))

    #                 # Apply the rule to the dataset D
    #                 delta_new = defaultdict(lambda: defaultdict(list))
    #                 naive_join(new_rule, D=I_minus_D, delta_new=delta_new, D_index=None)
    #                 print_dataset(delta_new)
