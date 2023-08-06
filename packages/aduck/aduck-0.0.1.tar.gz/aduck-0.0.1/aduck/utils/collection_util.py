from typing import Callable, Any
from collections.abc import Sequence


def group_by(dicts: [{}], keys: list or str, key_fn: Callable[[dict], Any] = None) -> {}:
    """
    eg.
    dicts = [{'a':2},{'a':1},{'a':1},{'a':1}]
    for k,v in group_by(dicts,'a').items():
        print(k,v)
    :param key_fn:
    :param dicts:
    :param keys:
    :return: {(keys):[items]}
    """
    r = {}
    for v in dicts:
        if keys:
            if isinstance(keys, Sequence) and not isinstance(keys, str):
                key = tuple(v[k] for k in keys)
            else:
                key = v[keys]
        elif key_fn:
            key = key_fn(v)
        if key not in r:
            r[key] = [v]
        else:
            r[key].append(v)
    return r


def subtract(a, b):
    """a-b"""
    if not b:
        return a
    return [v for v in a if v not in set(b)]


def unique(a):
    """unique a keep previous order"""
    if not a:
        return a
    s = set()
    r = []
    for v in a:
        if v in s:
            continue
        s.add(v)
        r.append(v)
    return r


def pick(m, keys, keep=True):
    r = {}
    for k in keys:
        if k in m:
            r[k] = m[k]
        else:
            if keep:
                r[k] = None
    return r


def pick_values(m, keys, keep=True):
    r = [None] * len(keys)
    for i, k in enumerate(keys):
        if k in m:
            r[i] = m[k]
    return r


def zip_dict(d: dict):
    """{a:1,b:2,c:3}->[[a,b,c],[1,2,3]]"""
    [fields, values] = zip(*[[k, d[k]] for k in d])
    return [list(fields), list(values)]


def zip2dict(a, b) -> dict:
    """[a,b,c],[1,2,3]->{a:1,b:2,c:3}"""
    return dict(zip(a, b))


def object2dict(obj, ignore_=True, ignore__=True, ignoreFunc=True):
    """convert object to dict"""
    d = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if ignore_ and name.startswith('_') or ignore__ and name.startswith('__') or ignoreFunc and callable(value):
            continue
        d[name] = value
    return d


def dict2object(obj, d):
    """Update object with dict. """
    obj.__dict__.update(d)
    return obj


def gather(a, key, index):
    """
    gather elements by key and index from a(list)
    :param a: list
    :param key: key in list element
    :param index:
    :return:
    """
    m = {}
    for v in a:
        m[v[key]] = v
    return [m[i] if i in m else None for i in index]
