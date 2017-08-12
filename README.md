Framework for modelling Kripke structure and modal logic formula
================================================================
[![Build Status](https://travis-ci.org/erohkohl/ai-modal-logic.svg?branch=master)](https://travis-ci.org/erohkohl/ai-modal-logic)
[![codecov](https://codecov.io/gh/erohkohl/ai-modal-logic/branch/master/graph/badge.svg)](https://codecov.io/gh/erohkohl/ai-modal-logic)

This framework provides a tool for modelling Kripke structures, modal and multi modal
logic formulas in Python. The aim of this framework is to describe the knowledge base
of multi agent systems and it's model, after one agent made an announcement. Their
knowledge base is mapped by a Kripke structure and one agents announcement is wrapped in
a multi modal logic formula.

#### Modelling Kripke structure
A Kripke Frame describes a simple directed graph and it's extension, Kripke structure,
assigns to each node a sub set a propositional variables. In Kripke's semantic a node is
call world, because it describes on possible scenario in the knowledge base. A propositional
variable is true in one world, if it is in the world's assign sub set of variables.

<img src="./doc/ks_example.png" width="300">

The following code snipped shows, how you can build the above Kripke structure. The Python syntax
allows to model the transition relations of a Kripke frame very similar to it's mathematical description.
To model a valid Kripke frame, you have to ensure, that each node name in the transition relation
appears in the list of worlds.

```python
from src.kripke import World, KripkeStructure

worlds = [
  World('1', {'p': True, 'q': True}),
  World('2', {'p': True, 'q': False}),
  World('3', {'p': False, 'q': True})
]

relations = {('1', '2'), ('2', '1'), ('1', '3'), ('3', '3')}
ks = KripkeStructure(worlds, relations)
```
I decided to model the set of propositional variable as dict, therefore it is not necessary to explicit assign false to a variable.  Moreover World('2', {'p': False}) and World('2', {}) are equivalent.

#### Describe modal logic formula and check it's semantic over one world
Further more this framework allows you to check wether a node of your Kripke structure forces a given modal logic formula. Therefore you can map the this formula with the framework as following code snipped shows. To get the Kripke semantic of a formula over one world just call *semantic()* and pass in the Kripke structure and the name of the world, you want to check.

<img src="./doc/formula_example.png" width="250">

```python
from src.formula import *

formula = Implies(
  Diamond(Atom('p')),
  And(
    Box(Box(Atom('q'))),
    Diamond(Atom('q'))
  )
)

assert True == formula.semantic(ks, '1')
```

#### Modelchecking
Moreover this framework allows to process new knowledge in addition to the current knowledge base, thus it applies a modal logic formula to a Kripke structure (knowledge base) and returns a model. This model is a valid Kripke structure, in terms all of it's worlds forces the formula. Therefore the function *solve()* removes the minimum subset of worlds, that prevent the Kripke structure
to force the formula.

```python
model = ks.solve(formula)
```

#### Modelling multimodal logic
Further the framework extends the classic modal logic by the semantics of Box_a and Diamond_a operators for describing multi agent systems. You can find their implementation in the Pyhton file [src.fromula](https://github.com/erohkohl/ai-modal-logic/blob/master/src/formula.py). To use this operators it is necessary to build a Kripke structure with additional transition relation for each agent. To illustrate the usage of framework's multi modal logic implementation I implemented the *three wise men puzzle*.

##### Example: Three wise men with hat
The data model of this example is located in [src.model](https://github.com/erohkohl/ai-modal-logic/blob/master/src/model.py) and the Pyhton file [test_model.py](https://github.com/erohkohl/ai-modal-logic/blob/master/test/test_model.py) proves it's results.

This puzzle is about three wise men, all of them wear either a red or a white hat. All in all there are two white and three red hats. Each wise men is only able to see the hats of his two neighbors and has to guess the color of his own hat. You can see the Kripke structure, that describes this knowledge base, in the picture below. For example the world name *RWW* denotes, that in this scenario the first wise man wears a red hat, the second and third wise men a white hat. The transition relation is defined by equivalence of two worlds for one agent. For example World *RWW* and *RRW* are equivalent for agent 2, because he can't distinguish these two possible scenarios.

<img src="./doc/wise_men.png" width="550">

This first wise man announces, that he doesn't know the color of his hat. This announcement implies, that either the second or third wise men has to wear a red hat. This first wise men would only be able to know the color of his hat, in case all of his neighbors wear white hats. Therefore we add the following formula to their knowledge base and apply it to the Kirpke structure.

```python
# First announcement implies, that second or third wise men wears a red hat
f = Box_star(Or(Atom('2:R'), Atom('3:R')))
model = ks.solve(f)
```

This model contains all worlds of the original Kirpke structure expect *WWW* and *RWW*. The second wise man admits, that he also doesn't know the color of his hat, although he know, that he or the third wise man has to wear a red hat. This announcement implies, that the third wise man knows his hat color. Thus the model of this formula only contains the green worlds.

```python
# First announcement implies, that second or third wise men wears a red hat
g = Box_a('3', Atom('3:R')
model = ks.solve(And(f, g))
```

#### Test-driven development

While developing this framework I made use of the test-driven approach. Thus this repository contains 56 py.test test case to ensure, that the framework works as expected, and for documentation purpose. Before you are able to run all tests, make sure you have installed the setup.py, which only contains py.test as dependency.

```bash
$ python setup.py install
$ py.test -v
```
test/test_and.py::test_semantic_p_and_q <span style="color:green">PASSED</span> <br />
test/test_atom.py::test_atom_init <span style="color:green">PASSED</span> <br />
test/test_atom.py::test_ks_one_world <span style="color:green">PASSED</span> <br />
test/test_atom.py::test_atom_is_false_if_q_not_in_V <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_one_world_true <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_one_world_false <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_one_world_reflex_edge_true <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_one_world_reflex_edge_false <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_two_worlds_true <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_two_worlds_false <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_three_worlds_true <span style="color:green">PASSED</span> <br />
test/test_box.py::test_semantic_box_p_three_worlds_false <span style="color:green">PASSED</span> <br />
test/test_box_a.py::test_semantic_box_a_true <span style="color:green">PASSED</span> <br />
test/test_box_a.py::test_semantic_box_a_false <span style="color:green">PASSED</span> <br />
test/test_box_a.py::test_semantic_box_a_two_agents <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_empty_relations <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_one_agent <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_two_agents_phi_not_hold <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_two_agents_box_phi_hold <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_two_agents_box_phi_not_hold <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_three_agents_box_phi_hold <span style="color:green">PASSED</span> <br />
test/test_box_star.py::test_box_star_three_agents_box_phi_not_hold <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_one_world_true <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_one_world_false <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_one_world_reflex_edge_true <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_one_world_reflex_edge_false <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_two_worlds_true <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_two_worlds_false <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_three_worlds_true <span style="color:green">PASSED</span> <br />
test/test_diamond.py::test_semantic_diamond_p_three_worlds_false <span style="color:green">PASSED</span> <br />
test/test_diamond_a.py::test_semantic_box_a_empty_relations <span style="color:green">PASSED</span> <br />
test/test_diamond_a.py::test_semantic_box_a_true <span style="color:green">PASSED</span> <br />
test/test_diamond_a.py::test_semantic_box_a_false <span style="color:green">PASSED</span> <br />
test/test_diamond_a.py::test_semantic_box_a_two_agents <span style="color:green">PASSED</span> <br />
test/test_implies.py::test_semantic_box_p_implies_p <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_kripke_structure_init <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_ks_wrong_type <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_get_power_set_of_worlds <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_eq_one_agent <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_eq_two_agents <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_eq_two_agents_not_eq <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_eq_empty_set <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_remove_node_trivial_case <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_remove_node_one_agent <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_remove_node_trivial_case_two_agent <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_remove_node_reflexive_edge <span style="color:green">PASSED</span> <br />
test/test_kripke.py::test_nodes_not_follow_formula <span style="color:green">PASSED</span> <br />
test/test_model.py::test_add_symmetric_edges <span style="color:green">PASSED</span> <br />
test/test_model.py::test_add_symmetric_is_already <span style="color:green">PASSED</span> <br />
test/test_model.py::test_add_reflexive_edges_one_agent <span style="color:green">PASSED</span> <br />
test/test_model.py::test_add_reflexive_edges_two_agents <span style="color:green">PASSED</span> <br />
test/test_model.py::test_solve_with_model_first_ann <span style="color:green">PASSED</span> <br />
test/test_model.py::test_solve_with_model_second_ann <span style="color:green">PASSED</span> <br />
test/test_not.py::test_semantic_not_q <span style="color:green">PASSED</span> <br />
test/test_or.py::test_semantic_p_or_q <span style="color:green">PASSED</span> <br />
test/test_readme.py::test_example_for_readme <span style="color:green">PASSED</span> <br />
