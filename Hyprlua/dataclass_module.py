from pathlib import Path
from .base_module import *


REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally

@register
@dataclasses.dataclass
class Comment(Base):
    keyword: ClassVar[str] = '#'

    def parse(self, line, parser_class):
        self._parse(line)
        return self

    def add_comment(self, line:str):
        if line.startswith('#'):
            return line
        else:
            return '#' + ' ' + line

    def __str__(self):
        line = super().__str__()

        if self.is_single_line:
            line = self.add_comment(line)
        if self.is_multiline:
            lines = line.split('\n')
            lines = [self.add_comment(l) for l in lines[:-1]]
            line = '\n'.join(lines)
        return line


@register
@dataclasses.dataclass
class File(Base):
    name: str = ''
    location:Path = Path()
    keyword: ClassVar[str] = 'source'
    lines:list = dataclasses.field(default_factory=list)

    def parse(self, line:str, parser_class):
        # source logic
        ...

    def add_line(self, line_obj:type(Base)):
        self.lines.append(line_obj)

    def __str__(self):
        return self._str_lines(self.lines)

@register
@dataclasses.dataclass
class Monitor(Base):
    keyword: ClassVar[str] = 'monitor'

    name= ''
    resolution= ''
    position= ''
    scale= ''

    def parse(self, line:str, parser_class):
        self._parse(line)
        self.name, self.resolution, self.position, self.scale = parser_class.var_inline_parse(line)
        return self

    def __str__(self):
        return f'monitor = {self.name}, {self.resolution}, {self.position}, {self.scale}'

@register
@dataclasses.dataclass
class Env(Base):

    keyword: ClassVar[str] = 'env'
    var_name = ''
    var_value = ''

    def parse(self, line:str, parser_class):
        self._parse(line)
        self.var_name, self.var_value = parser_class.var_inline_parse(line)
        return self

    def __str__(self):
        return f'env = {self.var_name},{self.var_value}'

@register
@dataclasses.dataclass
class Var(Base):

    keyword: ClassVar[str] = '$'
    var_name = ''
    var_value = ''

    def parse(self, line:str, parser_class):
        self._parse(line)
        _vars = line.split('=')
        self.var_name, self.var_value = _vars[0].strip()[1:], _vars[1].strip()
        return self

    def __str__(self):
        return f'${self.var_name} = {self.var_value}'

