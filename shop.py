import logging

class SymbolMeta(type):
    def __getattr__(cls, name):
        if name.startswith("__"):
            super(SymbolMeta, type).__getattr__(name)
        return cls(name=name)

class k(object):
    __metaclass__ = SymbolMeta

    def __repr__(self):
        chain = self._chain()
        names = [k_.name for k_ in chain]
        return "k<%s>" % ".".join(names)

    def __init__(self, name=None, prev=None):
        self.name = name
        self.prev = prev

    def __getattr__(self, name):
        return k(name=name, prev=self)

    def __call__(self, obj):
        if self.prev:
            res = self.prev(obj)
        else:
            res = obj
        logging.debug(str(self), res)
        if res is not None:
            attr_or_none = getattr(res, self.name, None)
            if attr_or_none is None and hasattr(res, '__getitem__'):
                attr_or_none = res.get(self.name, None)
            return attr_or_none
        else:
            return res

    def _chain(self):
        if self.prev:
            return self.prev._chain() + [self]
        else:
            return [self]
    def _path(self):
        chain = self._chain()
        names = [k_.name for k_ in chain]
        return "%s" % "_".join(names)

    def __add__(self, other):
        raise NotImplementedError
        


def d(*args):
    return lambda o: { arg._path(): arg(o) for arg in args }
