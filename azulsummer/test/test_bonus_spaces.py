from azulsummer.models.board import Board
from azulsummer.models.bonus_spaces import (
    _PILLAR_POSITIONS,
    _WINDOW_POSITIONS,
    BonusSpace,
    Pillar,
    Window,
)


def test_single_bonus_space_is_surrounded():
    b = Board()
    bs = BonusSpace()
    for position in _PILLAR_POSITIONS[0]:
        b.place_tile(*position)
    found, = bs.surrounded_spaces(b)
    assert found == Pillar(tuple(p.flatten() for p in _PILLAR_POSITIONS[0]))

def test_multiple_bonus_spaces_are_surrounded():
    # Set all window adjacent tiles on a board and confirms they are found
    # by BonusSpace.surrounded_spaces()
    b = Board()
    bs = BonusSpace()
    windows = set()
    for position_group in _WINDOW_POSITIONS:
        positions = []
        for position in position_group:
            b.place_tile(*position)
            positions.append(position.flatten())
        windows.add(Window(tuple(positions)))
    found = set(bs.surrounded_spaces(b))
    assert found == windows
