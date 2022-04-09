"""Frequently, Qt will simply return an integer where something far more
specific is expected. The enumId function identifies the expected value
from an integer and the possible expected values. For example:
enumId(262144, QMessageBox.StandardButton) returns ...Abort
with ... indicating the group, here: QMessageBox.StandardButton
"""
from icecream import ic as ic_

ic_.configureOutput(includeContext=True)


def enumId(enum: int, grp: any, debug=False) -> any:
  """Finds the member of grp with __hash__ equal to enum"""
  ic = ic_ if debug else lambda *args: None
  for (key, val) in grp.__dict__.items():
    if val and key != 'values':
      try:
        if enum == val.__hash__():
          ic(val.__repr__())
          return val
      except Exception as e:
        ic(key)
