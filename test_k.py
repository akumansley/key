import k


class Obj(dict):

  def __getattr__(self, attr):
    try:
      return self[attr]
    except KeyError:
      raise AttributeError

  def __setattr__(self, attr, value):
    self[attr] = value


def test_attribute_access():
  o = Obj()
  o.foo = 'bar'
  assert k.foo(o) == 'bar'
  assert k.baz(o) == None


def test_default():
  o = Obj()
  o.foo = 'bar'
  assert k.foo(o, default=True) == 'bar'
  assert k.bar(o, default=True) is True


def test_nested_access():
  o, c = Obj(), Obj()
  c.foo = 'bar'
  o.child = c
  assert k.child.foo(o) == 'bar'
  assert k.child.bar(o) == None
  assert k.foo.bar(o) == None


def test_list_indexing():
  o = Obj()
  a, b = Obj(), Obj()
  ls = [a, b]
  o.ls = ls
  assert k[0](ls) == a
  assert k.ls[0](o) == a


def test_self():
  o = Obj()
  assert k._(o) == o


def test_addition():
  o = Obj()
  o.foo = 'bar'
  o.bar = 'baz'
  o.baz = 'quux'
  assert (k.foo + k.bar +
          k.baz)(o) == {'foo': 'bar', 'bar': 'baz', 'baz': 'quux'}


def test_addition_and_nesting():
  o, c = Obj(), Obj()
  c.foo = 'bar'
  o.foo = 'bar'
  o.child = c
  assert (k.foo + k.child.foo)(o) == {'foo': 'bar', 'child_foo': 'bar'}

def test_deep_addition_and_nesting():
  a, b, c = Obj(), Obj(), Obj()
  a.foo = 'bar'
  b.foo = 'bar'
  c.foo = 'baz'
  a.bar = 'qux'
  b.bar = 'quux'
  c.bar = 'quux'
  ls = [a, b, c]
  assert (k.foo + k.bar)(ls) == [{
    "foo": "bar",
    "bar": "qux",
  }, {
    "foo": "bar",
    "bar": "quux",
  }, {
    "foo": "baz",
    "bar": "quux",
  }]


def test_nested_list():
  o, a, b = Obj(), Obj(), Obj()
  a.foo = 'bar'
  b.foo = 'baz'
  o.children = [a, b]
  assert k.children.foo(o) == ['bar', 'baz']


def test_flatten():
  o, a, b = Obj(), Obj(), Obj()
  w, x, y, z = Obj(), Obj(), Obj(), Obj()
  w.foo = 'bar'
  x.foo = 'bar'
  y.foo = 'bar'
  z.foo = 'bar'
  a.children = [w, x]
  b.children = [y, z]
  o.children = [a, b]
  assert k.children.children.foo(o) == [['bar', 'bar'], ['bar', 'bar']]
  assert k.children.children(flatten=True).foo(o) == ['bar', 'bar', 'bar', 'bar']
