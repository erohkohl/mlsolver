from src.formula.atom import Atom

def test_atom_init():
    atom = Atom("p");
    assert atom.name == "p"