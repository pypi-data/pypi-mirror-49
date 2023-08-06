#!/usr/bin/env python3


class Dictionary(dict):
    @classmethod
    def load(cls, f):
        import json
        if hasattr(f, 'read'):
            return json.load(f, object_hook=cls)
        else:
            with open(f, 'r') as fp:
                return json.load(fp, object_hook=cls)

    def where(self, expr):
        return Dictionary({k: v for k, v in self.items() if expr(k, v)})

    def select(self, expr):
        return List(expr(k, v) for k, v in self.items())

    def extend(self, **items):
        result = Dictionary(self) + items
        return result

    def map_keys(self, expr):
        return Dictionary({expr(k): v for k, v in self.items()})

    def __dir__(self):
        return super().__dir__() + list(self.keys())

    def __getattr__(self, attr):
        x = self.get(attr)
        if type(x) is list:
            wrapped = List(x)
            self[attr] = wrapped
            return wrapped
        else:
            return x

    def __setattr__(self, attr, value):
        if type(value) is list:
            self[attr] = List(value)
        elif type(value) is dict:
            self[attr] = Dictionary(value)
        else:
            self[attr] = value


class List(list):
    def where(self, expr):
        return List(x for x in self if expr(x))

    def select(self, expr):
        return List(expr(x) for x in self)

    def single(self):
        assert(len(self) == 1)
        return self[0]

    def first(self):
        return self[0]

    def many(self, expr):
        result = []
        for x in self.select(expr):
            result.extend(x)
        return List(result)

    def join(self, others, expr, select=None):
        result = []
        select = select or merge_dicts
        for this in self:
            result.extend([select(this, other) for other in others if expr(this, other)])
        return List(result)


def merge_dicts(x, y):
    x_keys = set(x.keys())
    return Dictionary(**x, **{(k if k not in x_keys else k + '_'): v for k, v in y.items()})


def test_dictionary_getattr():
    d = Dictionary()
    d['a'] = 123
    assert d.a == 123


def test_dictionary_where():
    d = Dictionary(a=1, b=2, c=3)
    w = d.where(lambda k, v: v >= 2)
    assert 'a' not in w
    assert 'b' in w
    assert 'c' in w


def test_dicrionary_dir():
    d = Dictionary(a=1, b=2, c=3)
    assert 'a' in dir(d)
    assert 'b' in dir(d)
    assert 'c' in dir(d)
    assert 'where' in dir(d)
    assert 'select' in dir(d)


def test_json_where_select():
    import io
    json_stream = io.StringIO('''
        {
            "data": [
                {"a": 1},
                {"a": 2},
                {"a": 3}
            ]
        }
    ''')
    d = Dictionary.load(json_stream)
    assert type(d.data) is List
    w = d.data.where(lambda x: x.a < 3).select(lambda x: x.a)
    assert 1 in w
    assert 2 in w
    assert 3 not in w


def test_merge_dicts():
    x = {'a': 1, 'b': 2, 'c': 3}
    y = {'c': 4, 'd': 5, 'e': 6}
    m = merge_dicts(x, y)
    assert m.a == 1
    assert m.b == 2
    assert m.c == 3
    assert m.c_ == 4
    assert m.d == 5
    assert m.e == 6


def test_extend():
    x = Dictionary(a=1, b=2, c=3)
    e = x.extend(d=4, e=5)
    assert e.a == 1
    assert e.b == 2
    assert e.c == 3
    assert e.d == 4
    assert e.d == 5


def test_join():
    import io
    json_stream = io.StringIO('''
        {
            "X": [
                {"id": 1, "a": 1},
                {"id": 1, "a": 2},
                {"id": 2, "a": 3},
                {"id": 2, "a": 4}
            ],
            "Y": [
                {"id": 1, "x_id": 2, "b": 1},
                {"id": 2, "x_id": 2, "b": 2},
                {"id": 3, "x_id": 1, "b": 3},
                {"id": 4, "x_id": 1, "b": 4}
            ]
        }
    ''')
    d = Dictionary.load(json_stream)
    j = d.X.where(lambda x: x.id == 1).join(d.Y, lambda x, y: x.id == y.x_id, lambda x, y: (x.a, y.b))
    assert (1, 3) in j
    assert (2, 4) in j
    assert (3, 1) not in j


def test_map_keys():
    d = Dictionary({"1": "a", "2": "b"})
    m = d.map_keys(int)
    assert 1 in m
    assert 2 in m
    assert m[1] == "a"
    assert m[2] == "b"


def test_change_list_and_reread():
    d = Dictionary({'a': [1, 2, 3]})
    d.a.append(4)
    assert len(d.a) == 4
