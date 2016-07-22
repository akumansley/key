import logging
import itertools
import sys


class SymbolMeta(type):

  def __getattr__(cls, name):
    if name.startswith("__"):
      super(SymbolMeta, type).__getattr__(name)
    return cls(name=name)

  def __getitem__(cls, idx):
    return cls(name=idx)


class KResult(dict):
  pass


def flatmap(func, iterable):
  return list(itertools.chain.from_iterable(map(func, iterable)))


class DictCombiner(object):

  def __repr__(self):
    return "(%s + %s)" % (self.left, self.right)

  def __init__(self, left, right):
    self.left = left
    self.right = right

  def __call__(self, obj):
    def merge(child, self_result):
      child_result = child(obj)
      if isinstance(child_result, KResult):
        return KResult(self_result.items() + child_result.items())
      else:
        return KResult(self_result.items() + [(child._path(), child_result)])

    self_result = KResult()
    self_result = merge(self.left, self_result)
    self_result = merge(self.right, self_result)
    return self_result

  def __add__(self, other):
    return DictCombiner(self, other)


class k(object):
  __metaclass__ = SymbolMeta

  def __repr__(self):
    chain = self._chain()
    names = [str(k_.name) for k_ in chain]
    return "k<%s>" % ".".join(names)

  def __init__(self, name=None, prev=None):
    self.name = name
    self.prev = prev
    self.flatten = None
    self.default = None

  def __getattr__(self, name):
    return k(name=name, prev=self)

  def __getitem__(self, idx):
    return k(name=idx, prev=self)

  def try_hard_to_get(self, obj):
    if self.name == "_":
      return obj
    attr_or_none = getattr(obj, str(self.name), self.default)
    if attr_or_none is self.default and hasattr(obj, '__getitem__'):
      try:
        attr_or_none = obj.__getitem__(self.name)
      except (IndexError, KeyError):
        return self.default
      except TypeError:
        if isinstance(obj, list):
          if self.flatten is True:
            return flatmap(self.try_hard_to_get, obj)
          else:
            return map(self.try_hard_to_get, obj)
    return attr_or_none

  def __call__(self, *args, **kwargs):
    flatten = kwargs.pop('flatten', None)
    if self.flatten is None:
      self.flatten = flatten

    default = kwargs.pop('default', None)
    if self.default is None:
      self.default = default

    if len(args) == 0:
      return self
    elif len(args) == 1:
      obj = args[0]
      if self.prev:
        res = self.prev(obj)
      else:
        res = obj
      if res is not None:
        return self.try_hard_to_get(res)
      else:
        return res

  def _chain(self):
    if self.prev:
      return self.prev._chain() + [self]
    else:
      return [self]

  def _path(self):
    chain = self._chain()
    names = [str(k_.name) for k_ in chain]
    return "%s" % "_".join(names)

  def __add__(self, other):
    return DictCombiner(self, other)
