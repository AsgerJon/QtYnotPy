"""The menu subclass of QMenu is used by the menubar class."""
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMenu


class Menu(QMenu):
  """The menu bar uses this class to create the files, edit and other
  members of the menubar"""

  @staticmethod
  def iconFromFile(fid):
    """Returns a QIcon loaded from the given filename"""
    pix = QPixmap(fid)
    return QIcon(pix)

  Icons = {
    'save': iconFromFile('./icons/filesave.png'),
    'open': iconFromFile('./icons/fileopen.png'),
    'new': iconFromFile('./icons/filenew.png'),
  }

  @classmethod
  def files(cls, main):
    """Class method creating a file menu containing items like new, save,
    save as and open actions configured as appropriate to the parent base
    window."""
    out = cls(main)
    out.setTitle('Files')
    main.addAction(out.addAction(cls.Icons['new'], 'New'))
    main.addAction(out.addAction(cls.Icons['open'], 'Open'))
    main.addAction(out.addAction(cls.Icons['save'], 'Save'))
    main.addAction(out.addAction(cls.Icons['save'], 'Save As'))
    return out

  @classmethod
  def edit(cls, main):
    """Class method creating a file menu containing items like new, save,
    save as and open actions configured as appropriate to the parent base
    window."""
    out = cls(main)
    out.setTitle('Edit')
    main.addAction(out.addAction(cls.Icons['props'], 'Properties'))
    return out

  @classmethod
  def help(cls, main):
    """Class method creating a file menu containing items like new, save,
    save as and open actions configured as appropriate to the parent base
    window."""
    out = cls(main)
    out.setTitle('Edit')
    main.addAction(out.addAction(cls.Icons['docs'], 'Documentation'))
    return out

  def __init__(self, main):
    QMenu.__init__(self)
    self.main = main
