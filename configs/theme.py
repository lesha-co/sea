from .cell_state import CellState
from enum import Enum


class Theme(Enum):
    MAIN = {
        CellState.CELL_DECK.value: '███',
        CellState.CELL_DECK_DEAD.value: '▒▒▒',
        CellState.CELL_EMPTY.value: '   ',
        CellState.CELL_FOG.value: '   ',
        CellState.CELL_MISS.value: ' ● '
    }
    TESTING = {
        CellState.CELL_DECK.value: '[#]',
        CellState.CELL_DECK_DEAD.value: '[x]',
        CellState.CELL_EMPTY.value: '[ ]',
        CellState.CELL_FOG.value: '[?]',
        CellState.CELL_MISS.value: '[.]'
    }