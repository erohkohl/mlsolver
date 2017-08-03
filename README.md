Framework for modelling Kripke structure and modal logic formula
================================================================
[![Build Status](https://travis-ci.org/erohkohl/ai-modal-logic.svg?branch=master)](https://travis-ci.org/erohkohl/ai-modal-logic)
[![codecov](https://codecov.io/gh/erohkohl/ai-modal-logic/branch/master/graph/badge.svg)](https://codecov.io/gh/erohkohl/ai-modal-logic)

Provides a small framework for modelling ks and modal logic formulas


#### Modelling Kripke structure
TODO definition of kss

<img src="./doc/ks_example.png" width="380">

```python
    worlds = [
        World('1', {'p': True, 'q': True}),
        World('2', {'p': True}),
        World('3', {'q': True})
    ]

    relations = {'a': {('1', '2'), ('2', '1'), ('1', '3'), ('3', '3')}}
    ks = KripkeStructure(worlds, relations)
```

#### Describe modal logic formula
<img src="./doc/formula_example.png" width="380">
```python
    formula = Implies(
        Diamond(Atom('p')),
        And(
            Box(Box(Atom('q'))),
            Diamond('q')
        )
    )

    assert True == formula.semantic(ks, '1')
```

#### Check semantic of formula over one world


#### Example: Three wise men with hat

#### Testdriven development
<img src="./doc/tests.png" width="980">
