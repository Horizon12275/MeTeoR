from meteor_reasoner.canonical.utils import find_periods
from meteor_reasoner.canonical.canonical_representation import CanonicalRepresentation
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes.atom import Atom
from meteor_reasoner.canonical.utils import fact_entailment
from meteor_reasoner.utils.operate_dataset import print_dataset, save_dataset_to_file

data = [
    "A(x)@0",
    "B(x)@0",
    "C(x)@0"
]
program = [
           "D(X):-ALWAYS[-1,-1] A(X)",
            "D(X):-ALWAYS[-1,-1] B(X)",
            "E(X):-ALWAYS[-1,-1] B(X)",
            "E(X):-ALWAYS[-1,-1] C(X)",

            "A(X):-ALWAYS[-1,-1] D(X)",
            "B(X):-ALWAYS[-1,-1] D(X)",
            "B(X):-ALWAYS[-1,-1] E(X)",
            "C(X):-ALWAYS[-1,-1] E(X)",
           ]
D = load_dataset(data)
Program = load_program(program)

print("D")

print_dataset(D)

CR = CanonicalRepresentation(D, Program)
CR.initilization()
D1, common, varrho_left, left_period, left_len, varrho_right, right_period, right_len = find_periods(CR)

print("D1 before entailment")
print_dataset(D1)

if varrho_left is None and varrho_right is None:
    print("This program is finitely materialisable for this dataset.")
    print("D1")
    print_dataset(D1)
else:
    if varrho_left is not None:
        print("left period:", str(varrho_left))
        for key, values in left_period.items():
            print(str(key), [str(val) for val in values])
    else:
        print("left period:", "[" + str(CR.base_interval.left_value - CR.w) + "," + str(CR.base_interval.left_value),
              ")")
        print("[]")

    if varrho_right is not None:
        print("right period:", str(varrho_right))
        for key, values in right_period.items():
            print(str(key), [str(val) for val in values])
    else:
        print("right period:", "(" + str(CR.base_interval.right_value),
              "," + str(CR.base_interval.right_value + CR.w) + "]")
        print("[]")

fact = "A(x)@4"
predicate, entity, interval = parse_str_fact(fact)
print("predicate:", predicate)
print("entity:", entity)
print("interval:", interval)

F = Atom(predicate, entity, interval)
print("Entailment:", fact_entailment(D1, F, common, left_period, left_len, right_period, right_len))

print("D1 after entailment")
print_dataset(D1)
