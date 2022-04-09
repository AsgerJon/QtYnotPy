"""This class provides for the menubars and actions"""
from PySide6.QtWidgets import QMenuBar

from menu import Menu


class MenuBar(QMenuBar):
  """MenuBar inherits from QMenuBar. This classes uses the menu
  re-implementations to build the menu bar along with QAction."""

  @classmethod
  def Basic(cls, main):
    """Creates a basic menu bar using basic menus"""
    out = cls(main)
    out.addMenu(Menu.files(main))
    out.addMenu(Menu.edit(main))
    out.addMenu(Menu.help(main))
    out.addMenu(Menu.about(main))
    return out

  def __init__(self, main):
    QMenuBar.__init__(self)
    self.main = main
    self.setWhatsThis('Menu Bar')
    self.setStatusTip('Menu Bar')
    self.setToolTip('Menu Bar')
