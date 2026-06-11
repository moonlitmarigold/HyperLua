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

    def parse(self, line:str, parser_class):
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

    def parse(self, line:str, parser_class):
        self.var_name, self.var_value = [x.strip() for x in line.split('=')]
        return self

    def __str__(self):
        return f'{self.var_name} = {self.var_value}'

@dataclasses.dataclass
class Category(Base):
    category_name = ''

    def parse(self, lines:list, category_name:str, parser_class):
        self.category_name = category_name.replace('{', '').strip()
        self._parse(lines)
        return self

    def __str__(self):
        str_lines = super().__str__()
        return f'{self.category_name} ' + '{\n' + str_lines + '}\n'