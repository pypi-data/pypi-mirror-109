from __future__ import annotations

from typing import Generic, TypeVar, Union, overload

from ._cell import Cell

CT = TypeVar("CT", bound="Cell")


__all__ = ("Board",)


class Board(Generic[CT]):
    def __init__(self, cell_type: type[CT], num_rows: int, num_cols: int) -> None:
        self.num_rows: int = num_rows
        self.num_cols: int = num_cols

        self.grid: list[list[CT]] = [[] for _ in range(num_rows)]

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row].append(cell_type(self, row, col))

    @overload
    def __getitem__(self, index: tuple[slice, slice]) -> list[list[CT]]:
        ...

    @overload
    def __getitem__(self, index: tuple[slice, int]) -> list[CT]:
        ...

    @overload
    def __getitem__(self, index: tuple[int, slice]) -> list[CT]:
        ...

    @overload
    def __getitem__(self, index: tuple[int, int]) -> CT:
        ...

    def __getitem__(self, index: tuple[Union[int, slice], Union[int, slice]]) -> Union[CT, list[CT], list[list[CT]]]:
        row, col = index

        if isinstance(row, slice):
            rows = self.grid[row]
            return [row[col] for row in rows]  # type: ignore

        return self.grid[row][col]  # type: ignore

    @property
    def rows(self) -> list[list[CT]]:
        return [self[row, :] for row in range(self.num_rows)]

    @property
    def cols(self) -> list[list[CT]]:
        return [self[:, col] for col in range(self.num_cols)]

    @property
    def cells(self) -> list[CT]:
        return [cell for row in self.grid for cell in row]
