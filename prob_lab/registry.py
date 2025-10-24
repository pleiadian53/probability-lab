
from typing import Callable, Dict

class Registry:
    def __init__(self):
        self._items: Dict[str, Callable] = {}
    def register(self, name: str):
        def deco(fn: Callable):
            self._items[name] = fn
            return fn
        return deco
    def get(self, name: str):
        if name not in self._items:
            raise KeyError(f"{name} not found in registry. Available: {list(self._items)}")
        return self._items[name]
    def names(self):
        return list(self._items)

distribution_registry = Registry()
