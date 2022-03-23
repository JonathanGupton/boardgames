import numpy as np
import pytest

from azulsummer.models.actionvalues import (
    DiscardExcessTilesValues,
    DrawFromFactoryDisplayValues,
    DrawFromSupplyValues,
    DrawFromCenterValues,
    PassValues,
    PlayTileToBoardValues,
)


@pytest.mark.parametrize(
    "method,args",
    [
        (DiscardExcessTilesValues, (np.array([1, 1, 1, 1, 1, 1]),)),
        (DrawFromFactoryDisplayValues, (0, np.array([1, 1, 1, 1, 1, 1]))),
        (DrawFromSupplyValues, (np.array([1, 1, 1, 1, 1, 1]),)),
        (DrawFromCenterValues, (np.array([1, 1, 1, 1, 1, 1]),)),
        (PassValues, ()),
        (PlayTileToBoardValues, (1, 1, 1)),
        (PlayTileToBoardValues, (3, 5, 6)),

    ],
)
def test_action_value_classes(method, args):
    av = method(*args)
    print()
    print(repr(av))
    print(av)
    print()
    assert repr(av)
    assert str(av)
