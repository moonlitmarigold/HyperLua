import dataclasses
import logging
from typing import ClassVar
logger = logging.getLogger('HyprLua')

@dataclasses.dataclass
class EmptyLine:

    commented: bool = False

    def __str__(self):
        if not self.commented:
            return ''
        else:
            return '#'


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

    def

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

    def filter_out_keyword(self, line:str):
        if line.startswith(self.keyword):
            return line[len(self.keyword):].strip()
        else:
            return line

@dataclasses.dataclass
class MultiLineBase:

    keyword: ClassVar[str] = ''   # not a field — just a class-level constant
    category_obj = None

    def parse(self, lines:list, parser_class):
        self.category_obj = parser_class.var_multiline_parse(lines)
        return self

    def __str__(self):
        return str(self.category_obj)

