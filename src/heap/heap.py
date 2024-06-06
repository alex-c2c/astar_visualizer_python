#!/usr/bin/env python3

from typing import Generic, TypeVar, Callable

T = TypeVar('T')

class GenericHeap(Generic[T]):
    def __init__(self, elements:list[T], cmp_func:Callable[[T, T], bool]) -> None:
        super().__init__()
        self.cmp_func = cmp_func
        self.elements:list[T] = elements
        self.fix()

    def __str__(self) -> str:
        return " ".join(str(x) for x in self.elements)

    def __len__(self) -> int:
        return self.elements.__len__()

    def fix(self) -> None:
        end:int = len(self.elements) - 1
        for i in range((len(self.elements) - 2 // 2), -1, -1):
            self.__sift_down__(i, end)

    def push(self, value:T) -> None:
        self.elements.append(value)
        self.fix()

    def pop(self) -> T|None:
        if len(self.elements) == 0:
            return None

        self.__swap__(0, len(self.elements) - 1)

        element:T = self.elements.pop(-1)

        self.__sift_down__(0, len(self.elements) - 1)

        return element

    def __sift_up__(self) -> None:
        child:int = len(self.elements) - 1
        parent:int = (child - 1) // 2
        while child >= 0 and self.cmp_func(self.elements[child], self.elements[parent]):
            self.__swap__(child, parent)
            child = parent
            parent = (child - 1) // 2

    def __sift_down__(self, curr:int, end:int) -> None:
        left:int = (curr * 2) + 1
        while left <= end:
            right:int = left + 1
            if right > end:
                right = -1

            swap:int = left
            if right != -1 and not self.cmp_func(self.elements[left], self.elements[right]):
                swap = right

            if self.cmp_func(self.elements[swap], self.elements[curr]):
                self.__swap__(swap, curr)
                curr = swap
                left = (curr * 2) + 1
            else:
                return

    def __swap__(self, i:int, j:int) -> None:
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]


def cmp(a:int, b:int) -> bool:
    return a < b


def main() -> None:
    a:list[int] = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
    gh:GenericHeap = GenericHeap[int](a, cmp)

    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")

    gh.push(100)
    print(f"{str(gh) = }")
    gh.push(50)
    print(f"{str(gh) = }")
    gh.push(10)
    print(f"{str(gh) = }")
    gh.push(90)
    print(f"{str(gh) = }")
    gh.push(80)
    print(f"{str(gh) = }")
    gh.push(20)
    print(f"{str(gh) = }")
    gh.push(40)
    print(f"{str(gh) = }")
    gh.push(70)
    print(f"{str(gh) = }")
    gh.push(60)
    print(f"{str(gh) = }")
    gh.push(30)
    print(f"{str(gh) = }")

    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")
    print(f"{gh.pop() = }")


if __name__ == "__main__":
    main()
