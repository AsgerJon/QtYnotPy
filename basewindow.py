"""BaseWindow collects important and general functionality used by all
applications. In particular, the instance method setupWidgets, must be
reimplemented by all subclasses."""
from __future__ import annotations

from abc import abstractmethod
import os
import pickle
from typing import NoReturn

from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QGridLayout, QMainWindow, QStatusBar, QWidget
from icecream import ic

from filedialogs import FileDialog
from mousefilter import ClickEvent


class BaseWindow(QMainWindow):
  """The reimplementation of QMainWindow"""

  @classmethod
  def fromUI(cls, uiFid, title=None):
    """Creates the window based on a provided ui file"""
    cmdString = 'pyside6-uic %s > _tempui.py' % (uiFid)
    os.system(cmdString)
    out = cls('QtYnotPy') if title is None else cls(title)
    import _tempui
    out.ui = _tempui.__dict__['Ui_%s' % (
      os.path.basename(uiFid)[:-3].capitalize())]()
    if not out.ui:
      raise Exception('No main window found!')
    out.setupWidgets = out.loadUi
    return out

  def __init__(self, title=None):
    if title is None:
      title = 'QtYnotPy'
    self._filters = ['JPEG image (*.jpg *.jpeg *.jpe)']
    QMainWindow.__init__(self)
    self.clicker = ClickEvent(self)
    ic(self.clicker.__call__)
    self.setWindowTitle(title)
    self.baseWidget = QWidget(self)
    self.baseLayout = QGridLayout(self.baseWidget)
    self.setCentralWidget(self.baseWidget)
    self.setGeometry(300, 300, 640, 480)
    self.timeLimit = 1
    self.ui = None
    self.openFileDialog = FileDialog.loadFile(self)
    self.loadDirDialog = FileDialog.loadDir(self)
    self.saveFileDialog = FileDialog.saveFile(self)
    self.dataFid = ''
    self.events = {}
    self.data = {}
    self.stBar = QStatusBar(self)
    self.setStatusBar(self.stBar)
    self.timer = QTimer()
    self.timer.setInterval(100)
    self.timer.timeout.connect(self.debug)

  def debug(self):
    """Happens every 100ms"""
    msg = 'Mouse waiting for %s'
    msg = msg % ('release' if self.clicker.active else 'press')
    self.statusBar().showMessage(msg)

  @property
  def filters(self):
    """The named filters used by file dialogs"""
    return self._filters

  @filters.setter
  def filters(self, value):
    self._filters = value

  def saveAsFunc(self):
    """This method saves the data in the self.data dictionary to pickled
    file on the disk."""
    files = self.saveFileDialog()
    if files:
      with open(self.dataFid, 'wb') as f:
        pickle.dump(self.data, f)

  def saveFunc(self):
    """This method actually saves the data on the disk. It is triggered by
    either the saveAsFunc or by the save action. """

  def loadFunc(self):
    """This method opens the disk allowing the user to select an
    existing file which is then opened but applying its values on the
    self.data variable"""
    files = self.openFileDialog()
    if files:
      with open(self.dataFid, 'rb') as f:
        self.data = pickle.load(f)

  def selectDir(self):
    """The method opens the disk allowing the user to select an existing
    folder."""
    files = self.openFileDialog = FileDialog.loadFile(self)

  def preSetup(self):
    """This function is triggered prior to the setupWidgets function. It
    is empty by default, and subclasses may reimplement it."""
    pass

  @abstractmethod
  def setupWidgets(self):
    """This abstract method must be reimplemented by subclasses"""

  def loadUi(self):
    """This method replaces setupWidgets when window is created from a ui
    file. If reimplemented, setupWidgets should point to this function."""
    self.ui.setupUi(self)

  def postSetup(self):
    """This function is triggered after the setupWidgets function. It
    is empty by default, and subclasses may reimplement it."""
    pass

  def showEvent(self, *event):
    """The showEvent runs preSetup, setupWidgets and postSetup in that
    order."""
    self.preSetup()
    self.setupWidgets()
    self.postSetup()
    self.timer.start()

  def mousePressEvent(self, event: QMouseEvent):
    """The event functions include a filter on their events, greatly
    simplifying their use. The press event starts a timer used by the
    mouse release event, such that if the mouse release event occurs after
    the time has expired its function does not trigger. Thus, mouse press
    event and mouse release events are collectively replaced by the
    mouse click event, which is a blank method by default, but which may
    be overwritten by subclasses."""
    self.clicker(event)

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """If timer has not run out, triggers"""
    if not self.clicker.active:
      return
    self.clicker(event)
    self.singleClick(self.clicker)

  def singleClick(self, e: ClickEvent) -> NoReturn:
    """This function should be reimplemented by subclasses as needed. """
    pass

  def doubleClick(self, e: ClickEvent) -> NoReturn:
    """This function should be reimplemented by subclasses as needed. """
    pass

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> NoReturn:
    """The event functions include a filter on their events, greatly
    simplifying their use. """
    self.clicker(event)
    self.doubleClick(self.clicker)

  def keyPressEvent(self, event: QKeyEvent) -> NoReturn:
    """The event functions include a filter on their events, greatly
    simplifying their use. """
