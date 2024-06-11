#!/usr/bin/env python3

from enum import Enum, auto

from .grid import GridScene, GridView
from .node import Node, NodeType
from astar.astar import start_path_finding, start_path_finding_heapq

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QPushButton, QMainWindow

import sys


class State(Enum):
    IDLE = auto()
    SETTING_START = auto()
    SETTING_END = auto()
    SETTING_BLOCKER = auto()


class VisualizerWindow(QMainWindow):
    def __init__(self, col:int, row:int) -> None:
        super().__init__()

        CONTROLS_MAX_WIDTH:int = 180
        LABELS_MAX_HEIGHT:int = 16

        self.setWindowTitle(f"A Star Visualizer - {col} x {row}")

        self._col:int = col
        self._row:int = row

        self._state:State = State.IDLE
        self._node_list:list[list[Node]] = []
        self._start_node:Node|None = None
        self._end_node:Node|None = None
        self._blockers:list[Node] = []
        self._paths:list[Node] = []

        self._label_node_start = QLabel()
        self._label_node_end = QLabel()
        self._label_node_blocker = QLabel()
        self._label_node_clear = QLabel()
        self._label_start = QLabel()
        
        self._button_node_start_set = QPushButton()
        self._button_node_start_clear = QPushButton()
        self._button_node_end_set = QPushButton()
        self._button_node_end_clear = QPushButton()
        self._button_node_blocker_set = QPushButton()
        self._button_node_blocker_clear = QPushButton()
        self._button_node_clear_all = QPushButton()
        self._button_node_clear_path = QPushButton()
        self._button_start_visualizer = QPushButton()

        # Start Node Section
        self._label_node_start.setText("Start Node: [ , ]")
        self._label_node_start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_node_start.setFixedSize(CONTROLS_MAX_WIDTH, LABELS_MAX_HEIGHT)
        self._button_node_start_set.setText("Set Start Node")
        self._button_node_start_set.clicked.connect(self._button_press_start_set)
        self._button_node_start_clear.setText("Clear Start Node")
        self._button_node_start_clear.clicked.connect(self._button_press_start_clear)

        # End Node Section
        self._label_node_end.setText("End Node: [ , ]")
        self._label_node_end.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label_node_end.setFixedSize(CONTROLS_MAX_WIDTH, LABELS_MAX_HEIGHT)
        self._button_node_end_set.setText("Set End Node")
        self._button_node_end_set.clicked.connect(self._button_press_end_set)
        self._button_node_end_clear.setText("Clear End Node")
        self._button_node_end_clear.clicked.connect(self._button_press_end_clear)

        # Blocker Node Section
        self._label_node_blocker.setFixedSize(CONTROLS_MAX_WIDTH, LABELS_MAX_HEIGHT)
        self._button_node_blocker_set.setText("Set Blocker Nodes")
        self._button_node_blocker_set.clicked.connect(self._button_press_blocker_set)
        self._button_node_blocker_clear.setText("Clear Blocker Nodes")
        self._button_node_blocker_clear.clicked.connect(self._button_press_blocker_clear)

        # Node Clearing Section
        self._label_node_clear.setFixedSize(CONTROLS_MAX_WIDTH, LABELS_MAX_HEIGHT)
        self._button_node_clear_path.setText("Clear Path")
        self._button_node_clear_path.clicked.connect(self._button_press_clear_path)
        self._button_node_clear_all.setText("Clear All")
        self._button_node_clear_all.clicked.connect(self._button_press_clear_all)

        # Start Section
        self._label_start.setFixedSize(CONTROLS_MAX_WIDTH, LABELS_MAX_HEIGHT)
        self._button_start_visualizer.setText("Start Visualizer")
        self._button_start_visualizer.clicked.connect(self._button_press_start_visualizer)

        # Combine Layouts
        layout_controls = QVBoxLayout()
        layout_controls.addWidget(self._label_node_start)
        layout_controls.addWidget(self._button_node_start_set)
        layout_controls.addWidget(self._button_node_start_clear)
        layout_controls.addWidget(self._label_node_end)
        layout_controls.addWidget(self._button_node_end_set)
        layout_controls.addWidget(self._button_node_end_clear)
        layout_controls.addWidget(self._label_node_blocker)
        layout_controls.addWidget(self._button_node_blocker_set)
        layout_controls.addWidget(self._button_node_blocker_clear)
        layout_controls.addWidget(self._label_node_clear)
        layout_controls.addWidget(self._button_node_clear_path)
        layout_controls.addWidget(self._button_node_clear_all)
        layout_controls.addWidget(self._label_start)
        layout_controls.addWidget(self._button_start_visualizer)

        controls = QWidget()
        controls.setLayout(layout_controls)
        controls.setBaseSize(CONTROLS_MAX_WIDTH, 200)

        # Scene
        self._grid_scene = GridScene(self._col, self._row, self._mouse_click_callback, self._mouse_move_callback)
        self._grid_view = GridView(self._grid_scene)

        layout_full = QHBoxLayout()
        layout_full.addWidget(controls)
        layout_full.addWidget(self._grid_view)

        # Grid
        for y in range(row):
            new_list:list[Node] = []
            for x in range(col):
                node:Node = Node(x, y)
                new_list.append(node)
                for graphic_item in node.get_graphic_item():
                    self._grid_scene.addItem(graphic_item)

            self._node_list.append(new_list)

        widget_full = QWidget()
        widget_full.setLayout(layout_full)

        self.setCentralWidget(widget_full)

    def _update_labels(self) -> None:
        if self._start_node is not None:
            self._label_node_start.setText(f"Start Node: [ {self._start_node.x} , {self._start_node.y} ]")
        else:
            self._label_node_start.setText(f"Start Node: [ , ]")

        if self._end_node is not None:
            self._label_node_end.setText(f"End Node: [ {self._end_node.x} , {self._end_node.y} ]")
        else:
            self._label_node_end.setText(f"End Node: [ , ]")

        if self._state == State.IDLE:
            self._button_node_start_set.setText(f"Set Start Node")
            self._button_node_end_set.setText(f"Set End Node")
            self._button_node_blocker_set.setText(f"Set Blocker Nodes")
        elif self._state == State.SETTING_START:
            self._button_node_start_set.setText(f"Setting Start Node")
            self._button_node_end_set.setText(f"Set End Node")
            self._button_node_blocker_set.setText(f"Set Blocker Nodes")
        elif self._state == State.SETTING_END:
            self._button_node_start_set.setText(f"Set Start Node")
            self._button_node_end_set.setText(f"Setting End Node")
            self._button_node_blocker_set.setText(f"Set Blocker Nodes")
        elif self._state == State.SETTING_BLOCKER:
            self._button_node_start_set.setText("Set Start Node")
            self._button_node_end_set.setText("Set End Node")
            self._button_node_blocker_set.setText("Setting Blocker Nodes")

    def _clear_node(self, node:Node|None) -> None:
        if node is not None:
            node.set_node_type(NodeType.EMPTY)

    def _set_start_node(self, new_node:Node) -> None:
        self._clear_node(self._start_node)

        new_node.set_node_type(NodeType.START)
        self._start_node = new_node

        self._update_labels()

    def _clear_start_node(self) -> None:
        self._clear_node(self._start_node)
        self._start_node = None

    def _set_end_node(self, new_node:Node) -> None:
        self._clear_node(self._end_node)

        new_node.set_node_type(NodeType.END)
        self._end_node = new_node

        self._update_labels()

    def _clear_end_node(self) -> None:
        self._clear_node(self._end_node)
        self._end_node = None

    def _append_blocker_node(self, new_node) -> None:
        if new_node.node_type != NodeType.EMPTY:
            return

        new_node.set_node_type(NodeType.BLOCKER)
        self._blockers.append(new_node)

    def _remove_blocker_node(self, node) -> None:
        if node.node_type != NodeType.BLOCKER:
            return

        node.set_node_type(NodeType.EMPTY)
        self._blockers.remove(node)

    def _clear_blocker_nodes(self) -> None:
        for n in self._blockers:
            self._clear_node(n)

        self._blockers.clear()

    def _clear_path_nodes(self) -> None:
        for n in self._paths:
            self._clear_node(n)

        self._paths.clear()

    def _button_press_start_set(self) -> None:
        if self._state == State.SETTING_START:
            self._state = State.IDLE
        else:
            self._state = State.SETTING_START

        self._update_labels()

    def _button_press_start_clear(self) -> None:
        self._state = State.IDLE
        self._clear_start_node()
        self._update_labels()

    def _button_press_end_set(self) -> None:
        if self._state == State.SETTING_END:
            self._state = State.IDLE
        else:
            self._state = State.SETTING_END

        self._update_labels()

    def _button_press_end_clear(self) -> None:
        self._state = State.IDLE
        self._clear_end_node()
        self._update_labels()

    def _button_press_blocker_set(self) -> None:
        if self._state == State.SETTING_BLOCKER:
            self._state = State.IDLE
        else:
            self._state = State.SETTING_BLOCKER

        self._update_labels()

    def _button_press_blocker_clear(self) -> None:
        self._state = State.IDLE
        self._clear_blocker_nodes()
        self._update_labels()

    def _button_press_clear_path(self) -> None:
        self._state = State.IDLE
        self._clear_path_nodes()
        self._update_labels()

    def _button_press_clear_all(self) -> None:
        self._state = State.IDLE
        self._clear_start_node()
        self._clear_end_node()
        self._clear_blocker_nodes()
        self._clear_path_nodes()
        self._update_labels()

    def _button_press_start_visualizer(self) -> None:
        if self._start_node is None:
            print(f"Start Node is [None]")
            return

        if self._end_node is None:
            print(f"End Node is [None]")
            return

        start:tuple[int, int] = (self._start_node.x, self._start_node.y)
        end:tuple[int, int] = (self._end_node.x, self._end_node.y)
        blockers = tuple((node.x, node.y) for node in self._blockers)

        return_path:tuple[tuple[int, int,], ...]|None = start_path_finding(self._col, self._row, start, end, blockers)
        #return_path_v2:tuple[tuple[int, int,], ...]|None = start_path_finding_heapq(self._col, self._row, start, end, blockers)

        if return_path is None:
            print(f"There is no return path!")
        else:
            self._display_return_path(return_path)

    def _display_return_path(self, path:tuple[tuple[int, int], ...]) -> None:
        # path pts are reverse ordered
        index:int = 0
        while index < len(path) - 2:
            pt_a:tuple[int, int] = path[index]
            pt_b:tuple[int, int] = path[index + 1]

            node = self._node_list[pt_a[1]][pt_a[0]]
            if node.node_type == NodeType.EMPTY:
                node.set_node_type(NodeType.PATH, pt_b)
                self._paths.append(node)

            index += 1

    def _mouse_click_callback(self, x:int, y:int) -> None:
        node = self._node_list[y][x]

        if self._state == State.IDLE:
            return

        elif self._state == State.SETTING_START:
            if node.node_type == NodeType.EMPTY:
                self._set_start_node(node)

        elif self._state == State.SETTING_END:
            if node.node_type == NodeType.EMPTY:
                self._set_end_node(node)

        elif self._state == State.SETTING_BLOCKER:
            if node.node_type == NodeType.EMPTY:
                self._append_blocker_node(node)
            elif node.node_type == NodeType.BLOCKER:
                self._remove_blocker_node(node)

    def _mouse_move_callback(self, x:int, y:int) -> None:
        node = self._node_list[y][x]

        if self._state == State.IDLE:
            return

        elif self._state == State.SETTING_START:
            if node.node_type == NodeType.EMPTY:
                self._set_start_node(node)

        elif self._state == State.SETTING_END:
            if node.node_type == NodeType.EMPTY:
                self._set_end_node(node)

        elif self._state == State.SETTING_BLOCKER:
            if node.node_type == NodeType.EMPTY:
                self._append_blocker_node(node)
            elif node.node_type == NodeType.BLOCKER:
                self._remove_blocker_node(node)


def main() -> None:
    app:QApplication = QApplication(sys.argv)


    window = VisualizerWindow(20, 20)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
