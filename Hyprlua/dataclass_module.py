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
    content: str = None
    multiline_content: list = None
    keyword: ClassVar[str] = ''   # not a field — just a class-level constant

    @property
    def is_single_line(self) -> bool:
        return self.content is not None

    @property
    def is_multiline(self) -> bool:
        return self.multiline_content is not None

    @property
    def _content(self):
        if self.is_single_line:
            return self.content
        elif self.is_multiline:
            return self.multiline_content
        else:
            return None

    def __str__(self):
        if self.is_single_line:
            return self.content
        elif self.is_multiline:
            return self._str_lines(self.multiline_content)
        else:
            return ''

    def _str_lines(self, lines:list):
        return_str = ''
        for line in lines:
            if isinstance(line, list) or isinstance(line, tuple):
                _list_str = self._str_lines(line)
                return_str += _list_str
            else:
                return_str += str(line) + '\n'
        return return_str

    def _parse(self, content:str | list):
        if isinstance(content, str):
            self.content = content
        elif isinstance(content, list) or isinstance(content, tuple):
            self.multiline_content = content
        else:
            logger.error('Invalid content type: {}'.format(type(content)))


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