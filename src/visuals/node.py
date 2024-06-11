#!/usr/bin/env python3

from enum import Enum, auto

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QFont
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSimpleTextItem, QGraphicsPolygonItem

NODE_SIZE:int = 32


class NodeType(Enum):
    EMPTY = auto()
    START = auto()
    END = auto()
    BLOCKER = auto()
    PATH = auto()
    PATH_OPEN = auto()
    PATH_CLOSED = auto()


class Node():
    def __init__(self, x:int, y:int):
        super().__init__()

        self.x = x
        self.y = y

        self._font:QFont = QFont()
        self._font.setPointSize(int(NODE_SIZE * 0.5))
        self._font.setBold(True)

        self._dot:QGraphicsEllipseItem = QGraphicsEllipseItem()
        self._text:QGraphicsSimpleTextItem = QGraphicsSimpleTextItem()
        self._poly:QGraphicsPolygonItem = QGraphicsPolygonItem()

        self.set_node_type(NodeType.EMPTY)

    def get_graphic_item(self) -> tuple[QGraphicsItem, ...]:
        return (self._dot, self._text, self._poly)

    def set_node_type(self, node_type:NodeType) -> None:
        self.node_type = node_type

        if self.node_type == NodeType.EMPTY:
            circle_scale = 0.2
            circle_size = NODE_SIZE * circle_scale
            circle_offset = (NODE_SIZE - circle_size) * 0.5

            self._dot.setBrush(QBrush(Qt.GlobalColor.gray))
            self._dot.setOpacity(0.15)
            self._dot.setRect(NODE_SIZE * self.x + circle_offset, NODE_SIZE * self.y + circle_offset, circle_size, circle_size)

            self._dot.setVisible(True)
            self._text.setVisible(False)
            self._poly.setVisible(False)

        elif self.node_type == NodeType.START:
            self._text.setText("S")
            self._text.setBrush(QBrush(Qt.GlobalColor.yellow))
            self._text.setFont(self._font)

            offset_x = (NODE_SIZE - self._text.boundingRect().width()) * 0.5
            offset_y = (NODE_SIZE - self._text.boundingRect().height()) * 0.5
            self._text.setPos(NODE_SIZE * self.x + offset_x, NODE_SIZE * self.y + offset_y)

            self._dot.setVisible(False)
            self._text.setVisible(True)
            self._poly.setVisible(False)

        elif self.node_type == NodeType.END:
            self._text.setText("E")
            self._text.setBrush(QBrush(Qt.GlobalColor.blue))
            self._text.setFont(self._font)

            offset_x = (NODE_SIZE - self._text.boundingRect().width()) * 0.5
            offset_y = (NODE_SIZE - self._text.boundingRect().height()) * 0.5
            self._text.setPos(NODE_SIZE * self.x + offset_x, NODE_SIZE * self.y + offset_y)

            self._dot.setVisible(False)
            self._text.setVisible(True)
            self._poly.setVisible(False)

        elif self.node_type == NodeType.BLOCKER:
            circle_scale = 0.5
            circle_size = NODE_SIZE * circle_scale
            circle_offset = (NODE_SIZE - circle_size) * 0.5

            self._dot.setBrush(QBrush(Qt.GlobalColor.red))
            self._dot.setOpacity(1)
            self._dot.setRect(NODE_SIZE * self.x + circle_offset, NODE_SIZE * self.y + circle_offset, circle_size, circle_size)

            self._dot.setVisible(True)
            self._text.setVisible(False)
            self._poly.setVisible(False)

        elif self.node_type == NodeType.PATH:
            circle_scale = 0.3
            circle_size = NODE_SIZE * circle_scale
            circle_offset = (NODE_SIZE - circle_size) * 0.5

            self._dot.setBrush(QBrush(Qt.GlobalColor.green))
            self._dot.setOpacity(0.65)
            self._dot.setRect(NODE_SIZE * self.x + circle_offset, NODE_SIZE * self.y + circle_offset, circle_size, circle_size)

            self._dot.setVisible(True)
            self._text.setVisible(False)
            self._poly.setVisible(False)

        elif self.node_type == NodeType.PATH_OPEN:
            ...
        elif self.node_type == NodeType.PATH_CLOSED:
            ...
