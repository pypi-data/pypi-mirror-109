from __future__ import annotations

from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from ._board import Board

__all__ = ("Cell",)


class Cell:
    def __init__(self, board: Board[Any], row: int, col: int) -> None:
        self.board: Board[Any] = board
        self.row: int = row
        self.col: int = col
