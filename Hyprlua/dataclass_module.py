import dataclasses
import logging
from pathlib import Path
from typing import ClassVar
logger = logging.getLogger('HyprLua')

@dataclasses.dataclass
class EmptyLine:

    def __str__(self):
        return ''

@dataclasses.dataclass
class Base:
    content: str = ''
    keyword: ClassVar[str] = ''   # not a field — just a class-level constant

    def __str__(self):
        return self.content

REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally

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
        return '\n'.join([str(line) for line in self.lines])

@register
@dataclasses.dataclass
class Comment(Base):
    keyword: ClassVar[str] = '#'
    content: str = ''

    def parse(self, line:str, parser_class):
        self.content = line

@register
@dataclasses.dataclass
class Monitor(Base):
    keyword: ClassVar[str] = 'monitor'
    content: str = ''

    def parse(self, line:str, parser_class):
        self.content = line