import numpy as np
import pytest

from azulsummer.models.enums import TileColor
from azulsummer.models.tile_array import TileArray, InvalidTileArrayLengthError


def test_tilearray_is_TileArray_type():
    ta = TileArray([0, 0, 0, 0, 0, 0])
    assert type(ta) is TileArray


@pytest.mark.parametrize("arr", [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]])
def test_array_of_length_not_eq_6_exception(arr):
    with pytest.raises(InvalidTileArrayLengthError):
        TileArray(arr)


def test_tile_array_from_dict():
    tiles = {TileColor.Orange: 1}
    assert np.array_equal(
        TileArray.from_dict(tiles=tiles), TileArray([1, 0, 0, 0, 0, 0])
    )
    assert not np.array_equal(
        TileArray.from_dict(tiles=tiles), TileArray([1, 1, 0, 0, 0, 0])
    )


def test_add_tile_array_to_np_array():
    tiles = {TileColor.Orange: 1}
    ta = TileArray.from_dict(tiles=tiles)
    assert np.array_equal(ta + np.array([1, 1, 0, 0, 0, 0]), [2, 1, 0, 0, 0, 0])
    assert np.array_equal(np.array([1, 1, 0, 0, 0, 0]) + ta, [2, 1, 0, 0, 0, 0])
