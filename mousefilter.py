"""The mouse filter provides a simplification of the handling of mouse
click events. """
from __future__ import annotations

import time

from PySide6.QtCore import QEvent
from PySide6.QtGui import QMouseEvent
from icecream import ic

ic.configureOutput(includeContext=True)


class ClickEvent:
  """This simpler event represents a mouse click. It is first created by
  the mouse press event on the main window after which it is recorded by
  the mainwindow class for the duration of the epoch setting. If then a
  mouse release event occurs before the time has run out, the instance
  created by the most recent mouse click is transmitted to it. Thus,
  each instance of ClickEvent should belong to a mainwindow constantly
  being updated with mouse interaction. """

  def __init__(self, main):
    self.main = main
    self._active = 0
    self.beginTime = 0
    self.left = False
    self.middle = False
    self.right = False
    self.forward = False
    self.backward = False
    self.xPress = None
    self.yPress = None
    self.xRelease = None
    self.yRelease = None
    self.xDoubleClick = None
    self.yDoubleClick = None

  def __call__(self, event: QMouseEvent):
    """The call method extract the desired information from the
    QMouseEvent. """
    if event.type() == QEvent.MouseButtonPress:
      self.beginTime = time.time()
      self.left = event.button() == 0
      self.middle = event.button() == 1
      self.right = event.button() == 2
      self.forward = event.button() == 3
      self.backward = event.button() == 4
      self.xPress = event.globalPosition().x()
      self.yPress = event.globalPosition().y()
    if event.type() == QEvent.MouseButtonDblClick:
      self.xDoubleClick = event.globalPosition().x()
      self.yDoubleClick = event.globalPosition().y()
    if event.type() == QEvent.MouseButtonRelease:
      self.xRelease = event.globalPosition().x()
      self.yRelease = event.globalPosition().y()

  @property
  def active(self):
    """Denotes whether or not the key released in time"""
    return time.time() - self.beginTime < self.main.timeLimit

  @active.setter
  def active(self, *_):
    raise TypeError('active is read-only!')

  def reset(self):
    """Resets the current values"""
    self.left = False
    self.middle = False
    self.right = False
    self.forward = False
    self.backward = False
    self.xPress = None
    self.yPress = None
    self.xRelease = None
    self.yRelease = None
    self.xDoubleClick = None
    self.yDoubleClick = None
