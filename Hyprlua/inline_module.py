import dataclasses
from .base_module import *

REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally

@register
@dataclasses.dataclass
class Match(Base):

    def check(self, line: str):
        if line.startswith('match'):
            return True
        return False

@register
@dataclasses.dataclass
class Var(Base):

    def check(self, line:str):
        if line.__contains__("="):
            return True
        return False

@dataclasses.dataclass
class Category(Base):

    def parse(self, lines:list, category_name:str, parser_class):
        return self