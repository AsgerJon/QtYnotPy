"""Creates a dialog window asking the user a question, accepting either
accept or reject."""
from typing import Callable

from PySide6.QtWidgets import QMessageBox


class Question(QMessageBox):
  """Creates a new question"""

  @classmethod
  def saveChanges(cls, slot):
    """Standard question for unsaved changes. """
    out = cls(slot, 'Unsaved Changes Found', 'Save Changes?')
    out.addButton(QMessageBox.Save)
    out.addButton(QMessageBox.Discard)
    out.addButton(QMessageBox.Cancel)
    return out

  def __init__(self, slot: Callable[..., any], title=None, text=None):
    QMessageBox.__init__(self)
    self._title = 'Question' if title is None else title
    self._text = 'Please Confirm' if text is None else text
    self.setWindowTitle(self.title)
    self.setText(self.text)
    self.finished.connect(slot)

  def __call__(self) -> int:
    """Calling the question raises it"""
    return self.open()

  @property
  def title(self) -> str:
    """Window title"""
    return self._title

  @title.setter
  def title(self, *_):
    raise TypeError('title is readonly!')

  @property
  def text(self) -> str:
    """Window text"""
    return self._text

  @text.setter
  def text(self, *_):
    raise TypeError('text is readonly!')
