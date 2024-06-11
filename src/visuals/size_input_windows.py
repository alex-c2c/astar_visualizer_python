#!/usr/bin/env python3

from collections.abc import Callable
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, QMainWindow


class SizeInputWindow(QMainWindow):
    def __init__(self, button_callback:Callable[[int, int], None]) -> None:
        super().__init__()

        self.button_callback = button_callback

        self.setWindowTitle("Input Grid Size")
        self.setMinimumSize(QSize(200,50))

        # COLUMN
        self.label_col:QLabel = QLabel()
        self.label_col.setText("Col Size")

        self.input_col:QLineEdit = QLineEdit()
        self.input_col.setPlaceholderText("Input a positive integer > 0")
        self.input_col.setValidator(QIntValidator(1, 1000, self))

        layout_col:QHBoxLayout = QHBoxLayout()
        layout_col.addWidget(self.label_col)
        layout_col.addWidget(self.input_col)

        # ROW
        self.label_row:QLabel = QLabel()
        self.label_row.setText("Row Size")

        self.input_row:QLineEdit = QLineEdit()
        self.input_row.setPlaceholderText("Input a positive integer > 0")
        self.input_row.setValidator(QIntValidator(1, 1000, self))

        layout_row:QHBoxLayout = QHBoxLayout()
        layout_row.addWidget(self.label_row)
        layout_row.addWidget(self.input_row)

        # BUTTON
        self.button_create:QPushButton = QPushButton()
        self.button_create.setText("Create Grid")
        self.button_create.clicked.connect(self.button_create_pressed)

        # COMBINE
        layout_col_row:QVBoxLayout = QVBoxLayout()
        layout_col_row.addLayout(layout_col)
        layout_col_row.addLayout(layout_row)
        layout_col_row.addWidget(self.button_create)

        container:QWidget = QWidget()
        container.setLayout(layout_col_row)

        self.setCentralWidget(container)


    def button_create_pressed(self):
        col_str:str = self.input_col.text()
        row_str:str = self.input_row.text()
        is_valid, col, row = self._sanatize_inputs(col_str, row_str)

        if is_valid:
            if self.button_callback is not None:
                self.button_callback(col, row)


    def _sanatize_inputs(self, col:str, row:str) -> tuple[bool, int, int]:
        if col == "":
            print(f"col cannot be empty")
            return False, -1, -1

        if not col.isdigit():
            print(f"col needs to be an integer")
            return False, -1, -1

        if  row == "":
            print(f"row cannot be empty")
            return False, -1, -1

        if not row.isdigit():
            print(f"row needs to be an integer")
            return False, -1, -1

        col_size:int = int(col)
        if col_size <= 1:
            print(f"col needs to be > 1")
            return False, -1, -1

        row_size:int = int(row)
        if row_size <= 1:
            print(f"row needs to be > 1")
            return False, -1, -1

        return True, col_size, row_size


def main() -> None:
    raise NotImplementedError(f"waiting to for someone to code me...")


if __name__ == "__main__":
    main()
