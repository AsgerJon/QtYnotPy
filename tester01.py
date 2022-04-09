"""The main file runs the code imported from other files. """
from __future__ import annotations

import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import QApplication

from basewindow import BaseWindow


def checkFile(fid):
  """Tries to open file"""
  file = QFile(fid)
  test = file.open(QIODevice.ReadOnly)
  file.close()
  print('Trying to open: %s' % (fid))
  print('Did open file' if test else 'Could not open file')


if __name__ == "__main__":
  import _tempui

  print(_tempui.__dict__['Ui_Welcome'])
  app = QApplication(sys.argv)
  widget = BaseWindow.fromUI('./uis/welcome.ui', 'QtYnotPy')
  widget.show()
  sys.exit(app.exec())
