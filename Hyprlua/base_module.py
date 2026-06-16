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
class Line:

    text: str
    comment:str = ''

@dataclasses.dataclass
class MultiLine:

    texts:list
    comments:list = ()


@dataclasses.dataclass
class Base:
    content: str = None
    multiline_content: list = None
    keyword: ClassVar[str] = ''   # not a field — just a class-level constant
    commands: str | list = None

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

    @staticmethod
    def filter_command(line:str):
        if line.__contains__('#'):
            return [x.strip() for x in line.split('#', maxsplit=1)]
        return line, ''

    def filter_commands(self, line:list):
        self.commands = list()
        _return = list()
        for l in line:
            if isinstance(l, str):
                r, c = self.filter_command(l)
                _return.append(r)
                self.commands.append(c)
            if isinstance(l, list):
                self.commands.append(self.filter_commands(l))

        return _return

    def _add_command(self, line:str, command = None):
        if command is None:
            return str(line + self.commands).strip()
        if command.strip() == '':
            return str(line).strip()
        return str(line + ' ' + '#' + ' ' + command).strip()

    def __str__(self):
        if self.is_single_line:
            return self._add_command(self.content)
        elif self.is_multiline:
            return self._str_lines(self.multiline_content, self.commands)
        else:
            return ''

    def _str_lines(self, lines:list, commands):
        return_str = ''
        for i, line in enumerate(lines):
            if isinstance(line, list) or isinstance(line, tuple):
                _list_str = self._str_lines(line, commands[i])
                return_str += _list_str
            else:
                return_str += self._add_command(line, commands[i])  + '\n'
        return return_str

    def _parse(self, content:str | list):
        if isinstance(content, str):
            self.content, self.commands = self.filter_command(content)
        elif isinstance(content, list) or isinstance(content, tuple):
            self.multiline_content = self.filter_commands(content)
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

