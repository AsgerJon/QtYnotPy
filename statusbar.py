"""General status bar. """
from PySide6.QtWidgets import QStatusBar


class StatusBar(QStatusBar):
  """StatusBar inherits from QStatusBar. """

  def __init__(self, main):
    QStatusBar.__init__(self)
    self.main = main
    self.setStyleSheet("""
      QStatusBar {
        background: rgb(63, 63, 63);
        color: white;
        border: 1px solid white;
      }
    """)
