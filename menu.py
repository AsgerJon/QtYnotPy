"""The menu subclass of QMenu is used by the menubar class."""
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QMenu


class Menu(QMenu):
  """The menu bar uses this class to create the files, edit and other
  members of the menubar"""

  @staticmethod
  def getIcon(key):
    iconFromFile = lambda fid: QIcon(QPixmap(fid))
    Icons = {
      'save': iconFromFile('./icons/filesave.png'),
      'open': iconFromFile('./icons/fileopen.png'),
      'new': iconFromFile('./icons/filenew.png'),
      'docs': iconFromFile('./icons/docs.png'),
      'props': iconFromFile('./icons/props.png'),
      'qt': iconFromFile('./icons/qt.png'),
    }
    return Icons[key]

  @classmethod
  def files(cls, main):
    """Class method creating a file menu containing items like new, save,
    save as and open actions configured as appropriate to the parent base
    window."""
    out = cls(main)
    out.setTitle('Files')
    out.setStatusTip('Files')
    out.setToolTip('Files')
    out.setWhatsThis('Files')
    main.saveAction = out.addAction(cls.getIcon('save'), 'Save')
    main.saveAsAction = out.addAction(cls.getIcon('save'), 'Save As')
    main.newAction = out.addAction(cls.getIcon('new'), 'New')
    main.openAction = out.addAction(cls.getIcon('open'), 'Open')
    main.addAction(main.saveAction)
    main.addAction(main.saveAsAction)
    main.addAction(main.newAction)
    main.addAction(main.openAction)
    return out

  @classmethod
  def edit(cls, main):
    """Edit menu."""
    out = cls(main)
    out.setTitle('Edit')
    out.setStatusTip('Edit')
    out.setToolTip('Edit')
    out.setWhatsThis('Edit')
    main.propAction = out.addAction(cls.getIcon('props'), 'Properties')
    main.addAction(main.propAction)
    return out

  @classmethod
  def help(cls, main):
    """The help menu"""
    out = cls(main)
    out.setTitle('Help')
    out.setStatusTip('Help')
    out.setToolTip('Help')
    out.setWhatsThis('Help')
    main.docAction = out.addAction(cls.getIcon('docs'), 'Documentation')
    main.addAction(main.docAction)
    return out

  @classmethod
  def about(cls, main):
    """The about menu"""
    out = cls(main)
    out.setTitle('About')
    out.setStatusTip('About')
    out.setToolTip('About')
    out.setWhatsThis('About')
    main.aboutQtAction = out.addAction(cls.getIcon('qt'), 'About Qt')
    main.addAction(main.aboutQtAction)
    return out

  def __init__(self, main):
    QMenu.__init__(self)
    self.main = main
