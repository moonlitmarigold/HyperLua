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

    def parse(self, line:str, parser_class):
        self.content = line

@register
@dataclasses.dataclass
class Env(Base):

    keyword: ClassVar[str] = 'env'
    var_name = ''
    var_value = ''

    def parse(self, line:str, parser_class):
        self._parse(line)
        self.var_name, self.var_value = parser_class.inline_parse(line)
        return self

@register
@dataclasses.dataclass
class Var(Base):

    keyword: ClassVar[str] = '$'
    var_name = ''
    var_value = ''

    def parse(self, line:str, parser_class):
        self._parse(line)
        line = line.strip('=').strip()
        self.var_name, self.var_value = line.split(',')
        return self

