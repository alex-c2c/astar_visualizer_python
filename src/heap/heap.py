#!/usr/bin/env python3

from typing import Generic, TypeVar, Callable

from random import randrange
#from timing.timing import timeit

T = TypeVar('T')

class GenericHeap(Generic[T]):
    def __init__(self, elements:list[T], _cmp_func:Callable[[T, T], bool]) -> None:
        super().__init__()
        self._cmp_func = _cmp_func
        self._elements:list[T] = elements
        self.fix()

    def __str__(self) -> str:
        return " ".join(str(x) for x in self._elements)

    def len(self) -> int:
        return self._elements.__len__()

    def fix(self) -> None:
        end:int = len(self._elements) - 1
        for i in range((len(self._elements) - 2 // 2), -1, -1):
            self._sift_down(i, end)

    def push(self, value:T) -> None:
        self._elements.append(value)
        self._sift_up()

    def pop(self) -> T:
        if len(self._elements) == 0:
            raise IndexError(f"Array length is 0, unable to pop")

        self._swap(0, len(self._elements) - 1)

        element:T = self._elements.pop(-1)

        self._sift_down(0, len(self._elements) - 1)

        return element

    def get_at_index(self, index:int) -> T:
        if index < 0 or index >= len(self._elements):
            raise IndexError(f"Index [{index}] out of bounds. Length: {self._elements.__len__()}")

        return self._elements[index]

    def _sift_up(self) -> None:
        child:int = len(self._elements) - 1
        parent:int = (child - 1) // 2
        while child >= 0 and self._cmp_func(self._elements[child], self._elements[parent]):
            self._swap(child, parent)
            child = parent
            parent = (child - 1) // 2

    def _sift_down(self, curr:int, end:int) -> None:
        left:int = (curr * 2) + 1
        while left <= end:
            right:int = left + 1
            if right > end:
                right = -1

            swap:int = left
            if right != -1 and not self._cmp_func(self._elements[left], self._elements[right]):
                swap = right

            if self._cmp_func(self._elements[swap], self._elements[curr]):
                self._swap(swap, curr)
                curr = swap
                left = (curr * 2) + 1
            else:
                return

    def _swap(self, i:int, j:int) -> None:
        self._elements[i], self._elements[j] = self._elements[j], self._elements[i]


def cmp(a:int, b:int) -> bool:
    return a < b


def main() -> None:
    a:list[int] = []
    gh:GenericHeap = GenericHeap[int](a, cmp)

    for _ in range(10000):
        random_num:int = randrange(1, 10_000)
        gh.push(random_num)
        print(f"pushing {random_num}, index at 0: {gh.get_at_index(0)}")


if __name__ == "__main__":
    main()
