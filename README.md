Framework for modelling Kripke structure and modal logic formula
================================================================
[![Build Status](https://travis-ci.org/erohkohl/ai-modal-logic.svg?branch=master)](https://travis-ci.org/erohkohl/ai-modal-logic)
[![codecov](https://codecov.io/gh/erohkohl/ai-modal-logic/branch/master/graph/badge.svg)](https://codecov.io/gh/erohkohl/ai-modal-logic)

Provides a small framework for modelling ks and modal logic formulas



#### Modelling Kripke structure
TODO definition of kss

<img src="./doc/ks_example.png" width="300">

```python
worlds = [
  World('1', {'p': True, 'q': True}),
  World('2', {'p': True}),
  World('3', {'q': True})
]

relations = {('1', '2'), ('2', '1'), ('1', '3'), ('3', '3')}
ks = KripkeStructure(worlds, relations)
```

#### Describe modal logic formula and check it's semantic over one world
<img src="./doc/formula_example.png" width="250">

```python
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
get KS with all worlds forces formula
```python
model = ks.solve(formula)
```

#### Modelling multimodal logic

#### Example: Three wise men with hat
<img src="./doc/wise_men.png" width="550">

#### Testdriven development
```bash
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
