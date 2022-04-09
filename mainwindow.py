"""This MainWindow is a sample of what an actual implementation should
look like. """
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from icecream import ic

from basewindow import BaseWindow

ic.configureOutput(includeContext=True)


class MainWindow(BaseWindow):
  """Inherits from BaseWindow class"""

  def __init__(self, title=None):
    title = 'Sample Window' if title is None else title
    BaseWindow.__init__(self, title)
    self.loader = QUiLoader()
    self.loader.addPluginPath('uis')
    self.welcomeFid = 'uis/welcome.ui'
    self.welcomeFile = QFile(self.welcomeFid)
    self.welcomeFile.open(QFile.ReadOnly)
    ic(self.welcomeFile)
    self.welcomeWindow = self.loader.load(self.welcomeFile)

  def setupWidgets(self):
    """Addds the welcome window"""
    self.baseLayout.addWidget(self.welcomeWindow, 0, 0, 1, 1)
