#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication
from visuals.visualizer_window import VisualizerWindow
from visuals.size_input_windows import SizeInputWindow
import sys
import argparse

size_input_windows:SizeInputWindow|None = None
visualizer_window:VisualizerWindow|None = None


def create_visualizer_window(col:int, row:int) -> None:
    print(f"create_visualizer_window - {col = } , {row = }")

    global size_input_windows
    global visualizer_window

    if size_input_windows is not None:
        is_close:bool = size_input_windows.close()
        if is_close:
            print(f"size_input_windows closed")

    visualizer_window = VisualizerWindow(col, row)
    visualizer_window.show()


def create_size_input_window() -> None:
    global size_input_windows
    size_input_windows = SizeInputWindow(create_visualizer_window)
    size_input_windows.show()


def main(col:int, row:int) -> None:
    app:QApplication = QApplication(sys.argv)

    if col > 1 and row > 1:
        create_visualizer_window(col, row)
    else:
        create_size_input_window()

    app.exec()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group()
    group.add_argument("-c", "--c", help="Column size, needs to be > 1", type=int, default=-1)
    group.add_argument("-r", "--r", help="Row size, needs to be > 1", type=int, default=-1)

    args = parser.parse_args()

    col:int = getattr(args, "c")
    row:int = getattr(args, "r")

    main(col, row)
