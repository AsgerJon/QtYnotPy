"""BaseWindow collects important and general functionality used by all
applications. In particular, the instance method setupWidgets, must be
reimplemented by all subclasses."""
from __future__ import annotations

from abc import abstractmethod
import os
import pickle
from typing import NoReturn

from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QDesktopServices, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QGridLayout, QMainWindow, QMessageBox, \
  QWidget
from icecream import ic

from filedialogs import FileDialog
from menubars import MenuBar
from mousefilter import ClickEvent
from statusbar import StatusBar

ic.configureOutput(includeContext=True)


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
    title = 'QtYnotPy' if title is None else title
    self._filters = ['JPEG image (*.jpg *.jpeg *.jpe)']
    QMainWindow.__init__(self)
    self.clicker = ClickEvent(self)
    self.timeLimit = 1
    self.setWindowTitle(title)
    #  Layouts
    self.baseWidget = QWidget(self)
    self.baseLayout = QGridLayout(self.baseWidget)
    self.setCentralWidget(self.baseWidget)
    self.setGeometry(300, 300, 640, 480)
    self.ui = None
    #  Dialogs
    self.openFileDialog = FileDialog.loadFile(self)
    self.loadDirDialog = FileDialog.loadDir(self)
    self.saveFileDialog = FileDialog.saveFile(self)
    #  Actions
    self.saveAction = QAction()
    self.saveAsAction = QAction()
    self.newAction = QAction()
    self.openAction = QAction()
    self.propAction = QAction()
    self.docAction = QAction()
    self.aboutQtAction = QAction()
    #  MenuBar
    self.setMenuBar(MenuBar.Basic(self))
    #  StatusBar
    self.setStatusBar(StatusBar(self))
    #  Data
    self.dataFid = ''
    self._requireFileName = True
    self._dataFilePath = None
    self._dataFileName = None
    self._dataFileExt = 'ext'
    self.data = {}
    self.getters = {}
    self.setters = {}
    #  Other
    self.events = {}
    #  Status Bar
    self.stBar = StatusBar(self)
    self.setStatusBar(self.stBar)

  def debug(self):
    """Happens every 100ms"""
    msg = 'Mouse waiting for %s'
    msg = msg % ('release' if self.clicker.active else 'press')
    self.statusBar().showMessage(msg)

  @property
  def requireFileName(self) -> bool:
    """Flag indicating that the current file name is default, such as
    untitled07. Should return false after first successful run of save as
    method. """
    return self._requireFileName

  @requireFileName.setter
  def requireFileName(self, value: bool) -> NoReturn:
    self._requireFileName = value

  @property
  def dataFileName(self):
    """The filename of the currently active instance. Contains only the
    filename itself, not the path nor the extension."""
    return os.path.splitext(os.path.basename(self.dataFilePath))[0]

  @dataFileName.setter
  def dataFileName(self, *_):
    raise TypeError('dataFileName should not be set directly!')

  @property
  def dataFileExt(self):
    """The file extension of the file."""
    return os.path.splitext(os.path.basename(self.dataFilePath))[1]

  @dataFileExt.setter
  def dataFileExt(self, value):
    raise TypeError('dataFileExt should not be set directly!')

  @property
  def dataFilePath(self):
    """The full path to the data file"""
    return self._dataFilePath

  @dataFilePath.setter
  def dataFilePath(self, value):
    self._dataFilePath = value

  @property
  def filters(self):
    """The named filters used by file dialogs"""
    return self._filters

  @filters.setter
  def filters(self, value):
    self._filters = value

  def unsavedChanges(self):
    """The instance data variable contains the most recently saved data.
    The save function first updates the contents of this variable,
    and then saves the variable to the disk. Thus, any discrepancy between
    the data variable and its sources indicates the presence of unsaved
    changes. """
    for (key, val) in self.data.items():
      if self.accessAppData(key, 'get')() != val:
        return True
    return False

  def maybeSave(self, btn: QMessageBox.StandardButton) -> bool:
    """Opens a confirmation dialog if unsaved changes are present. If the
    user accepts or if there are no saved changes present, returns True.
    Otherwise, returns False"""
    if not self.unsavedChanges():
      return True
    if btn == QMessageBox.StandardButton.Save:
      self.saveFunc()
    if btn == QMessageBox.StandardButton.Ignore:
      return True
    if btn == QMessageBox.StandardButton.Cancel:
      return False

  def saveChangesToData(self):
    """Updates the contents of the instance data variable as described by
    the getter functions of accessAppData. Used by the save file
    functions."""
    for (key, val) in self.data.items():
      self.data[key] = self.getters[key]()

  def applyValuesFromData(self):
    """Sets the values in the application to the values currently in the
    instance data variable. Used by the open function."""
    for (key, val) in self.data.items():
      self.data[key] = self.setters[key](val)

  def docFunc(self):
    """Opens documentation"""
    QDesktopServices.openUrl(QUrl.fromLocalFile('./README.md'))

  def propFunc(self):
    """Opens properties window"""
    QDesktopServices.openUrl(QUrl.fromLocalFile('./properties.txt'))

  def aboutQtFunc(self):
    """Opens properties window"""
    QMessageBox.aboutQt(self)

  def saveAsFunc(self):
    """This method saves the data in the self.data dictionary to pickled
    file on the disk."""
    files = self.saveFileDialog()
    if files:
      self.dataFilePath = os.path.abspath(files)
      self.requireFileName = False
      return self.saveFunc()
    return False

  def newFunc(self):
    """This method creates a new instance. Checks for unsaved changes and
    prompts user if necessary."""

  def saveFunc(self):
    """This method actually saves the data on the disk. It is triggered by
    either the saveAsFunc or by the save action. """
    if not self.unsavedChanges():
      return
    if self.requireFileName:
      return self.saveAsFunc()
    self.saveChangesToData()
    with open(self.dataFilePath, 'wb') as f:
      pickle.dump(self.data, f)
      return True

  def openFunc(self):
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

  def setupActions(self):
    """Connects actions to their relevant methods. This method is called
    automatically as part of the show event. It should also be called
    after changes are made to actions and menus."""
    self.saveAction.triggered.connect(self.saveFunc)
    self.saveAsAction.triggered.connect(self.saveAsFunc)
    self.newAction.triggered.connect(self.newFunc)
    self.openAction.triggered.connect(self.openFunc)
    self.propAction.triggered.connect(self.docFunc)
    self.docAction.triggered.connect(self.propFunc)
    self.aboutQtAction.triggered.connect(self.aboutQtFunc)

    for (key, val) in self.__dict__.items():
      if isinstance(val, QAction):
        val.setStatusTip(val.text())
        val.setWhatsThis(val.text())
        val.setToolTip(val.text())
        val.setIconText(val.__str__())

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
    self.setupActions()
    self.postSetup()

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
