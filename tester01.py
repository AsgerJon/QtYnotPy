"""The main file runs the code imported from other files. """
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

# def checkFile(fid):
#   """Tries to open file"""
#   file = QFile(fid)
#   test = file.open(QIODevice.ReadOnly)
#   file.close()
#   print('Trying to open: %s' % (fid))
#   print('Did open file' if test else 'Could not open file')
from basewindow import BaseWindow

if __name__ == "__main__":
  app = QApplication(sys.argv)
  widget = BaseWindow()
  widget.show()
  sys.exit(app.exec())
  #
  # ic()
  # app = QApplication(sys.argv)
  # ic()
  # widget = MainWindow(app)
  # widget.show()
  # sys.exit(app.exec())
