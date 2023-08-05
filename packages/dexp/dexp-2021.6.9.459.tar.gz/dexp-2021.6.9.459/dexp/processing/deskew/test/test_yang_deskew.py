from arbol import aprint

from dexp.datasets.operations.demo.demo_deconv import _demo_deconv
from dexp.datasets.operations.demo.demo_deskew import _demo_deskew
from dexp.processing.backends.cupy_backend import CupyBackend
from dexp.processing.backends.numpy_backend import NumpyBackend
from dexp.processing.deskew.demo.demo_classic_deskew import _classic_deskew
from dexp.processing.deskew.demo.demo_yang_deskew import _yang_deskew


def test_yang_deskew_numpy():
    with NumpyBackend():
        _yang_deskew(length=48, display=False)

def test_yang_deskew_cupy():
    try:
        with CupyBackend():
            _yang_deskew(length=48, display=False)

    except ModuleNotFoundError:
        aprint("Cupy module not found! demo ignored")


