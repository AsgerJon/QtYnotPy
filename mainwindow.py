"""This MainWindow is a sample of what an actual implementation should
look like. """

from PySide6.QtWidgets import QLabel, QLineEdit
from icecream import ic

from basewindow import BaseWindow

ic.configureOutput(includeContext=True)


class MainWindow(BaseWindow):
  """Inherits from BaseWindow class"""

  def __init__(self, title=None):
    title = 'Sample Window' if title is None else title
    BaseWindow.__init__(self, title)
    self.label = QLabel(self)
    self.label.setText('Hello World!')
    self.lineEdit = QLineEdit(self)
    self.lineEdit.setPlaceholderText('Test line edit')
    self.data = {'text': None}
    self.getters = {
      'text': self.lineEdit.text
    }
    self.setters = {
      'text': self.lineEdit.setText
    }

  def setupWidgets(self):
    """Reimplementation of setupWidgets"""
    self.baseLayout.addWidget(self.label, 0, 0, 1, 1)
    self.baseLayout.addWidget(self.lineEdit, 1, 0, 1, 1, )
