"""The main file runs the code imported from other files. """
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == "__main__":
  app = QApplication(sys.argv)
  widget = MainWindow('QtYnotPy')
  widget.show()
  sys.exit(app.exec())
