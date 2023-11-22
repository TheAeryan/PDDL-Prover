# PDDL-Prover
A python prover for evaluating FOL formulas on PDDL.

PDDL-Prover allows to construct arbitrary formulas in first-order logic (FOL) in Python, using a declarative syntax and including counting quantifiers. Then, the truth values of these formulas can be evaluated on a _knowledge base_, which represents a set of objects/contants and a set of true atoms (as in PDDL).

This results useful for evaluating conditions on PDDL states. For example, to check if in a given blocksworld state block A is on top of the table and under block B, we can do the following:

```
(ontable(A) & on(B,A)).evaluate(kb)
```

where `kb` is the knowledge base containing the objects and atoms of the blocksworld state. The line above will return `True` if the condition is met at the state, and `False` otherwise. You can find a more elaborate example below.

## Installation

The package is available in PyPI and can be installed with `pip install pddl-prover`.
Alternatively, you can clone this repository.

## Example of use

```
from pddl-prover import *

b0, b1, b2, b3, b4  =  Constant(0), Constant(1), Constant(2), Constant(3), Constant(4)
x, y  =  Variable('x'), Variable('y')

handempty  =  Predicate('handempty', 0) # The second argument is the arity
ontable  =  Predicate('ontable', 1)
on  =  Predicate('on', 2)
clear  =  Predicate('clear', 1)

# Note: atoms in the knowledge base can be represented either in tuple form or as instances of the class logic.Atom
kb  = ({b0,b1,b2},{('ontable', (0,)), ('on',(1,0)), ('on', (2,1)), ('clear',(2,)),
('handempty', tuple())})

print("Evaluation:", handempty().evaluate(kb)) # True
print("Evaluation:", (ontable(b0) & on(b1,b0)).evaluate(kb)) # True
print("Evaluation:", TE(x, on(x,b0)).evaluate(kb)) # There Exists some x for which on(x,b0) -> True
print("Evaluation:", (TE(x, ontable(x)) == 1).evaluate(kb)) # There exists <only> one object for which ontable(x) is True -> True (counting quantifier)
print("Number of true substitutions:", Count(on(x,y), x, y).evaluate(kb)[0]) # Returns the number of x and y substitutions for which on(x,y) is True -> 2