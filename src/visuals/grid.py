#!/usr/bin/env python3

from collections.abc import Callable

from .node import NODE_SIZE

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtWidgets import QGraphicsLineItem


class GridScene(QGraphicsScene):
    def __init__(self, col:int, row:int, mouse_click_callback:Callable[[int, int], None], mouse_move_callback:Callable[[int, int], None]):
        super().__init__(0, 0, NODE_SIZE * col, NODE_SIZE * row)

        self._mouse_click_callback = mouse_click_callback
        self._mouse_move_callback = mouse_move_callback

        self._is_mouse_clicked:bool = False
        self._is_mouse_moved:bool = False
        self._current_mouse_index:tuple[int, int] = (-1, -1)

        # Border
        group_border = QGraphicsItemGroup()
        p_black = QPen(Qt.GlobalColor.black)
        p_black.setWidth(3)

        l1 = QGraphicsLineItem(0, 0, self.width(), 0)
        l2 = QGraphicsLineItem(0, self.height(), self.width(), self.height())
        l3 = QGraphicsLineItem(0, 0, 0, self.height())
        l4 = QGraphicsLineItem(self.width(), 0, self.width(), self.height())

        l1.setPen(p_black)
        l2.setPen(p_black)
        l3.setPen(p_black)
        l4.setPen(p_black)

        group_border.addToGroup(l1)
        group_border.addToGroup(l2)
        group_border.addToGroup(l3)
        group_border.addToGroup(l4)

        self.addItem(group_border)

        # Grid Seperator
        group_seperator = QGraphicsItemGroup()
        for y in range(1, row):
            for x in range(1, col):
                lh = QGraphicsLineItem(0, y * NODE_SIZE, self.width(), y * NODE_SIZE)
                lh.setPen(p_black)
                lh.setOpacity(0.25)
                group_seperator.addToGroup(lh)

                lv = QGraphicsLineItem(x * NODE_SIZE, 0, x * NODE_SIZE, self.height())
                lv.setPen(p_black)
                lv.setOpacity(0.25)
                group_seperator.addToGroup(lv)

        self.addItem(group_seperator)

    def mousePressEvent(self, event) -> None:
        self._is_mouse_clicked = True
        self._is_mouse_moved = False

        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self._mouse_click_callback is not None and event is not None:
            pos_x:float = event.scenePos().x()
            pos_y:float = event.scenePos().y()

            if pos_x >= 0 and pos_x <= self.width() and pos_y >= 0 and pos_y <= self.height() and not self._is_mouse_moved:
                x, y = self._convert_pt_to_index(pos_x, pos_y)
                self._mouse_click_callback(x, y)

        self._is_mouse_clicked = False
        self._is_mouse_moved = False
        self._current_mouse_index = (-1, -1)

        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event) -> None:
        self._is_mouse_moved = True

        if event is not None and self._is_mouse_clicked:
            pos_x:float = event.scenePos().x()
            pos_y:float = event.scenePos().y()

            if pos_x >= 0 and pos_x <= self.width() and pos_y >= 0 and pos_y <= self.height():
                mouse_index = self._convert_pt_to_index(pos_x, pos_y)
                if mouse_index != self._current_mouse_index:
                    self._current_mouse_index = mouse_index
                    self._mouse_move_callback(mouse_index[0], mouse_index[1])

        return super().mouseMoveEvent(event)

    def _convert_pt_to_index(self, pos_x:float, pos_y:float) -> tuple[int, int]:
        x:int = int(pos_x / NODE_SIZE)
        y:int = int(pos_y / NODE_SIZE)

        return x, y


class GridView(QGraphicsView):
    def __init__(self, scene:GridScene):
        super(GridView, self).__init__()
        self.setMouseTracking(True)
        self.setScene(scene)


