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

    def build(self):
        return f'match = {{ {self.match_type} = "{self.match_value}" }},'

@register
@dataclasses.dataclass
class Color(Base):

    keyword: ClassVar[str] = 'col.'
    color_type:str = ''
    color:str|Gradient = ''
    gradient_as_color = False

    @staticmethod
    def check(line: str):
        if line.startswith('col.'):
            return True
        return False

    def parse(self, line:str):
        front, color = line.split('=')
        color = color.strip()
        if Gradient.check(color):
            self.gradient_as_color = True
            self.color = Gradient().parse(color)
        else:
            self.color = color
        front = front.strip()
        self.color_type = front.split('.')[1]
        return self

    def __str__(self):
        return f'col.{self.color_type} = {str(self.color)}'

    def build(self):
        if self.gradient_as_color:
            return f'{self.color_type} = {self.color.build()},'
        return f'{self.color_type} = {Gradient.return_color_value(self.color)},'

@register
@dataclasses.dataclass
class SingleColor(Base):

    keyword: ClassVar[str] = 'color'
    color_name:str = ''
    color:str = ''

    @staticmethod
    def check(line: str):
        if line.startswith('color'):
            return True
        return False

    def parse(self, line:str):
        self.color_name, self.color = [l.strip() for l in line.split('=')]
        return self

    def __str__(self):
        return f'{self.color_name} = {Gradient.return_color_value(self.color)}'

    def build(self):
        return self.__str__() + ','


@dataclasses.dataclass
class Category(Base):
    category_name = ''
    lines:list = None

    def parse(self, lines:list, category_name:str):
        self.category_name = category_name
        self.lines = lines
        return self

    def collect_colors(self, lines:list):
        new_lines = []
        colors = []
        for line in lines:
            if isinstance(line, Line) and isinstance(line.pars_obj, Color):
                colors.append(line)
            else:
                new_lines.append(line)
        return new_lines, colors


    def build(self):
        first_line:Line = self.lines[0].from_line(f'{self.category_name} = {{')
        build_list = [first_line.build()]
        lines, colors = self.collect_colors(self.lines[1:-1])

        if colors:
            build_list.append(first_line.from_line('col = {').add_indent().build())
            for color in colors:
                build_list.append(color.add_indent().build())
            build_list.append(first_line.from_line('},').add_indent().build())

        for line in lines:
            build_list.append(line.build())
        last_line = first_line.from_line('},')
        build_list.append(last_line.build())
        return '\n'.join(build_list)

    def __str__(self):
        return str_lines(self.lines)

@register
@dataclasses.dataclass
class Animation(Base):

    animation_rule:str = ''

    @staticmethod
    def check(line:str):
        if line.startswith('animation'):
            return True
        return False

    def parse(self, line:str):
        self.animation_rule = line
        return self

    def __str__(self):
        return f'{self.animation_rule}'

    def build(self):
        return f'-- {self.animation_rule}'

@register
@dataclasses.dataclass
class Bezier(Base):

    bezier = ''

    @staticmethod
    def check(line:str):
        if line.startswith('bezier'):
            return True
        return False

    def parse(self, line:str):
        self.bezier = line
        return self

    def __str__(self):
        return f'{self.bezier}'

    def build(self):
        return f'-- {self.bezier}'

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
        if self.var_value.__contains__('yes'):
            self.var_value = 'true'
        return self

    def __str__(self):
        return f'{self.var_name} = {self.var_value}'

    def build(self):
        return f'{self.var_name} = {self.return_var_value(self.var_value)},'