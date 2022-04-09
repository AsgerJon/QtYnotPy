"""File dialogs allow for saving and loading of files. There may be several
 types of file dialogs, such as save file, load/open file or select
 directory. However, they are sufficiently similarly that they may share a
 class being instantiated by each their own class method. Thus, FileDialog
 is a subclass of QFileDialog taking settings from their function and from
 the main window on which they are instantiated."""
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QFileDialog

if TYPE_CHECKING:
  from basewindow import BaseWindow


class FileDialog(QFileDialog):
  """Use the proper class method to instantiate file dialogs. Note,
  how the __call__ method runs the most primary function: Namely, opening
  the dialog and returning the file or directory chosen by the user,
  or returning None if no selection is made. """

  @classmethod
  def loadFile(cls, main: BaseWindow):
    """This class method creates a file loading dialog on the provided
    main window."""
    out = cls(main)
    out.setFileMode(QFileDialog.ExistingFile)
    out.setAcceptMode(QFileDialog.AcceptOpen)
    return out

  @classmethod
  def saveFile(cls, main: BaseWindow):
    """This class method creates a file loading dialog on the provided
    main window."""
    out = cls(main)
    out.setFileMode(QFileDialog.AnyFile)
    out.setAcceptMode(QFileDialog.AcceptSave)
    return out

  @classmethod
  def loadDir(cls, main: BaseWindow):
    """This class method creates a file dialog letting a user choose a
    directory with only folders being visible."""
    out = cls(main)
    out.setFileMode(QFileDialog.Directory)
    out.setAcceptMode(QFileDialog.AcceptOpen)
    out.setOption(QFileDialog.ShowDirsOnly, True)
    return out

  def __init__(self, main: BaseWindow):
    QFileDialog.__init__(self, main)
    self.main = main
    self.setViewMode(QFileDialog.Detail)
    self.setNameFilters(self.main.filters)

  def __call__(self):
    """Opens the dialog"""
    if self.exec():
      return self.selectedFiles()[0]
    return False
