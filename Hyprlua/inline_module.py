import dataclasses
from .base_module import *

REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally

@register
@dataclasses.dataclass
class Match(Base):

    match_type:str = ''
    match_value:str = ''

    @staticmethod
    def check(line: str):
        if line.startswith('match'):
            return True
        return False

    def parse(self, line:str):
        match, self.match_value = [x.strip() for x in line.split('=')]
        self.match_type  = match.split(':')[1].strip()
        return self

    def __str__(self):
        return f'match:{self.match_type}={self.match_value}'

@register
@dataclasses.dataclass
class Var(Base):

    var_name = ''
    var_value = ''

    @staticmethod
    def check(line:str):
        if line.__contains__("="):
            return True
        return False

    def parse(self, line:str):
        self.var_name, self.var_value = [x.strip() for x in line.split('=')]
        return self

    def __str__(self):
        return f'{self.var_name} = {self.var_value}'

@register
@dataclasses.dataclass
class Color(Base):

    keyword: ClassVar[str] = 'col'
    color_type:str = ''
    color:str = ''

    @staticmethod
    def check(line: str):
        if line.startswith('col.'):
            return True
        return False

    def parse(self, line:str):
        front, self.color = line.split('=')
        self.color = self.color.strip()
        front = front.strip()
        self.color_type = front.split('.')[1]
        return self


@dataclasses.dataclass
class Category(Base):
    category_name = ''
    lines:list = None

    def parse(self, lines:list, category_name:str):
        self.category_name = category_name
        self.lines = lines
        return self

    def __str__(self):
        return str_lines(self.lines)

@register
@dataclasses.dataclass
class WindowRule(Base):
    ...

@register
@dataclasses.dataclass
class Animation(Base):
    ...