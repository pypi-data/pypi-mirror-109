from typing import *

import hashlib


class QxHash(object):
  def __init__(self, algorithm: str):
    self._hash_o = getattr(hashlib, algorithm)
    assert callable(self._hash_o)

  def hash_s(self, s: Union[str, bytes]) -> str:
    if isinstance(s, str):
      s = s.encode('utf-8')
    h = self._hash_o()
    h.update(s)
    return h.hexdigest().lower()

  def hash_f(self, f: str) -> str:
    with open(f, 'rb') as fo:
      return self.hash_s(fo.read())
