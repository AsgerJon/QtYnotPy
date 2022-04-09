"""Pynarchy provides imaginative extra functionalities in Python that are
not supported by the general Python community."""


class Infix:
  def __init__(self, function):
    self.function = function

  def __call__(self, x, y):
    return self.function(x, y)

  def __ror__(self, other):
    return Infix(lambda x, self=self, other=other: self.function(other, x))
