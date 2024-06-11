#!/usr/bin/env python3

from __future__ import annotations, barry_as_FLUFL
from dataclasses import dataclass

from timing.timing import timeit
from heap.heap import GenericHeap

@dataclass
class PfNode:
    pt:Point
    parent:PfNode|None = None
    f:int = 0
    g:int = 0
    h:int = 0


@dataclass
class Point:
    x:int = -1
    y:int = -1

    def __repr__(self) -> str:
        return f"{self.x = } , {self.y = }"

    def __str__(self) -> str:
        return f"{self.x = } , {self.y = }"


def get_return_path(n:PfNode) -> tuple[tuple[int, int], ...]:
    path:list[tuple[int, int]] = []

    current_node:PfNode|None = n
    while current_node != None:
        path.append((current_node.pt.x, current_node.pt.y))
        current_node = current_node.parent

    return tuple(path)


def get_valid_adj_pts(curr_node:PfNode, steps:dict[str, Point], blockers:tuple[Point, ...], col:int, row:int) -> dict[str, Point]:
    children_dict:dict[str, Point] = {}
    block_dict:dict[str, bool] = {
        "t": False,
        "r": False,
        "b": False,
        "l": False
    }

    for k in steps:
        new_x:int = curr_node.pt.x + steps[k].x
        new_y:int = curr_node.pt.y + steps[k].y

        if new_x < 0 or new_x >= col or new_y < 0 or new_y >= row:
            continue

        child:Point = Point(new_x, new_y)
        if child in blockers:
            block_dict[k] = True
            continue

        if len(k) == 2:
            if block_dict[k[0]] and block_dict[k[1]]:
                continue

        children_dict[k] = child

    return children_dict


def get_index_in_heap(pt:Point, heap:GenericHeap[PfNode]) -> int:
    for i in range(heap.len()):
        node = heap.get_at_index(i)
        if node.pt == pt:
            return i

    return -1


@timeit
def start_path_finding(col:int, row:int, start:tuple[int, int], end:tuple[int, int], blockers:tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]|None:
    start_node:PfNode = PfNode(Point(start[0], start[1]))
    end_node:PfNode = PfNode(Point(end[0], end[1]))

    print(f"{start_node = }")
    print(f"{end_node = }")

    blocker_pts:tuple[Point, ...] = tuple(Point(b[0], b[1]) for b in blockers)

    print(f"{blocker_pts = }")

    steps:dict[str, Point] = {}
    steps["t"] = Point(0, -1)
    steps["r"] = Point(1, 0)
    steps["b"] = Point(0, 1)
    steps["l"] = Point(-1, 0)
    steps["tr"] = Point(1,  -1)
    steps["br"] = Point(1, 1)
    steps["bl"] = Point(-1, 1)
    steps["tl"] = Point(-1, -1)

    open_heap:GenericHeap = GenericHeap[PfNode]([start_node], cmp_func)
    close_list:list[PfNode] = []

    while open_heap.len() > 0:
        #print(f"{open_heap.len() = }")
        curr_node:PfNode = open_heap.pop()
        close_list.append(curr_node)

        if curr_node.pt == end_node.pt:
            return get_return_path(curr_node)

        valid_pts:dict[str, Point] = get_valid_adj_pts(curr_node, steps, blocker_pts, col, row)
        for key in valid_pts:
            child_pt:Point = valid_pts[key]

            if child_pt in close_list:
                continue

            g:int = 0
            if len(key) == 2:
                g = curr_node.g + 15
            else:
                g = curr_node.g + 10

            h:int = square(child_pt, end_node.pt)
            f:int = g + h

            existing_index:int = get_index_in_heap(child_pt, open_heap)
            if existing_index != -1:
                node:PfNode = open_heap.get_at_index(existing_index)
                if node.g > g:
                    node.g = g
                    node.h = h
                    node.f = f
                    node.parent = curr_node
                    open_heap.fix()
                else:
                    continue

            open_heap.push(PfNode(child_pt, curr_node, f, g, h))

    return None


def square(a:Point, b:Point) -> int:
    c:int = a.x - b.x
    d:int = a.y - b.y
    return c ** 2 + d ** 2


def cmp_func(a:PfNode, b:PfNode) -> bool:
    return a.f < b.f
