from typing import TypeVar

# Brython chokes on the Python 3.12 syntax
K = TypeVar("K")
V = TypeVar("V")


# taken from https://stackoverflow.com/a/5948050/2192464
class UniqueDict[K, V](dict[K, V]):
    def __setitem__(self, key: K, value: V):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")
