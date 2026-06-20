import dataclasses
import logging
from typing import ClassVar
logger = logging.getLogger('HyprLua')

@dataclasses.dataclass
class Indent:

    indent_count:int = 0
    indent_spaces:int = 4

    def __str__(self):
        return ' ' * self.indent_spaces * self.indent_count

    def add_indent(self):
        self.indent_count += 1
        return self


def str_lines(lines:list):
    return '\n'.join([str(x) for x in lines])

@dataclasses.dataclass
class EmptyLine:

    def set_commented(self):
        pass

    def __str__(self):
        return ''

    def add_indent(self):
        pass


@dataclasses.dataclass
class Line:

    text: str
    comment:str = ''
    pars_obj = None
    is_comment:bool = False
    indent:Indent = dataclasses.field(default_factory=Indent)

    def __post_init__(self):
        if self.text.__contains__('#') and not self.is_comment:
            self.text, self.comment = [x.strip() for x in self.text.split('#', 1)]

    def set_pars_obj(self, pars_obj):
        self.pars_obj = pars_obj().parse(self.text)
        return self

    def set_commented(self):
        self.is_comment = True
        return self

    def startswith(self, key):
        return self.text.startswith(key)

    def add_indent(self):
        self.indent.add_indent()
        return self


    @staticmethod
    def return_comment(_str):
        if _str.startswith('#'):
            return _str
        return '#' + ' ' + _str

    def __str__(self):
        if self.pars_obj is None:
            _str =  self.text
        else:
            _str:str = self.pars_obj.__str__().strip()

        if self.is_comment:
            _str =  self.return_comment(_str)
        if self.comment.strip() == '':
            return str(self.indent) + _str
        return str(self.indent) + _str + ' # ' + self.comment

@dataclasses.dataclass
class MultiLine:

    lines:list
    comments:list = ()
    is_comment:bool = False
    category_obj = None
    indent:Indent = dataclasses.field(default_factory=Indent)

    def __post_init__(self):
        for line in self.lines[1:-1]:
            line.add_indent()


    def __str__(self):
        if self.category_obj is None:
            return str_lines(self.lines)
        return self.category_obj.__str__()

    def set_commented(self):
        self.is_comment = True
        for _line in self.lines:
            _line.set_commented()
        return self

    def add_indent(self):
        for line in self.lines:
            line.add_indent()
        return self

    def set_category_obj(self, category_obj):
        self.category_obj = category_obj
        return self


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
    def var_inline_parse(line:str):
        line = line.split('=')[1].strip()
        _vars = line.split(',')
        _vars = [v.strip() for v in _vars]
        return _vars

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

