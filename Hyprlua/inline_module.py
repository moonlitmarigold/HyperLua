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

    def set(self, color_name, color):
        self.color_name = color_name
        self.color = color
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
    leaf = ''
    enabled = True
    speed = ''
    bezier_name = ''
    style = ''

    @staticmethod
    def check(line:str):
        if line.startswith('animation'):
            return True
        return False

    def parse(self, line:str):
        self.animation_rule = line
        parts = [x.strip() for x in line.split('=', 1)[1].split(',')]
        # A disabled animation may be given as just "NAME, 0" (no speed/curve).
        self.leaf = parts[0]
        self.enabled = len(parts) > 1 and parts[1] == '1'
        self.speed = parts[2] if len(parts) > 2 else ''
        self.bezier_name = parts[3] if len(parts) > 3 else ''
        self.style = parts[4] if len(parts) > 4 else ''
        return self

    def __str__(self):
        return f'{self.animation_rule}'

    def build(self):
        enabled_str = 'true' if self.enabled else 'false'
        result = f'hl.animation({{ leaf = "{self.leaf}", enabled = {enabled_str}'
        if self.speed:
            result += f', speed = {self.speed}'
        if self.bezier_name:
            result += f', bezier = "{self.bezier_name}"'
        if self.style:
            result += f', style = "{self.style}"'
        result += ' })'
        return result

@register
@dataclasses.dataclass
class Bezier(Base):

    bezier = ''
    curve_name = ''
    x0 = ''
    y0 = ''
    x1 = ''
    y1 = ''

    @staticmethod
    def check(line:str):
        if line.startswith('bezier'):
            return True
        return False

    def parse(self, line:str):
        self.bezier = line
        parts = [x.strip() for x in line.split('=', 1)[1].split(',')]
        self.curve_name = parts[0]
        self.x0, self.y0, self.x1, self.y1 = parts[1], parts[2], parts[3], parts[4]
        return self

    def __str__(self):
        return f'{self.bezier}'

    def build(self):
        return f'hl.curve("{self.curve_name}", {{ type = "bezier", points = {{ {{{self.x0}, {self.y0}}}, {{{self.x1}, {self.y1}}} }} }})'

@dataclasses.dataclass
class Var(Base):

    var_name = ''
    var_value = ''

    @staticmethod
    def check(line:str):
        if line.__contains__("="):
            return True
        return False

    def set(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
        return self

    def parse(self, line:str):
        self.var_name, self.var_value = [x.strip() for x in line.split('=')]
        if self.var_value.__contains__('yes'):
            self.var_value = 'true'
        if self.var_value.__contains__('no'):
            self.var_value = 'false'
        return self

    def __str__(self):
        return f'{self.var_name} = {self.var_value}'

    def build(self):
        return f'{self.var_name} = {self.return_var_value(self.var_value)},'

@dataclasses.dataclass
class Opacity(Base):

    active:Var = dataclasses.field(default_factory=lambda:Var().set("active", 1))
    inactive:Var = None
    keyword = 'opacity'

    def parse(self, line:str):
        logger.debug('Active before parsing: %s', self.active)
        logger.debug('Inactive before parsing: %s', self.inactive)
        parts = line.strip().split(' ')[1:]
        logger.debug('Parts: %s', parts)
        if len(parts) == 2:
            self.active = Var().set("active", float(parts[0]))
            self.inactive = Var().set("inactive", float(parts[1]))
        else:
            self.active = Var().set("active", float(parts[0]))
        logger.debug('Active after parsing: %s', self.active)
        logger.debug('Inactive after parsing: %s', self.inactive)
        return self

    def build(self):
        if not self.inactive:
            return f'{self.keyword} = {{ {self.active.build()} }},'
        return f'{self.keyword} = {{ {self.active.build()} {self.inactive.build()} }},'

@dataclasses.dataclass
class BorderColor(Base):

    active:SingleColor = None
    inactive:SingleColor = None
    keyword = 'border_color'

    def parse(self, line:str):
        parts = line.strip().split(' ')[1:]
        if len(parts) > 1:
            self.active = SingleColor().set("active", parts[0])
            self.inactive = SingleColor().set("inactive", parts[1])
        return self

    def build(self):
        if not self.inactive:
            return f'{self.keyword} = {{ {self.active.build()} }},'
        return f'{self.keyword} = {{ {self.active.build()} {self.inactive.build()} }},'

class Size(Base):

    num1 = int()
    num2 = int()
    keyword:str = 'size'

    def parse(self, line:str):
        parts = line.strip().split(' ')[1:]
        if len(parts) != 1:
            self.num1 = parts[0]
            self.num2 = parts[1]
            return self
        else:
            self.num1 = parts[0]
            return self

    def set_key(self, key:str):
        self.keyword = key
        return self

    def __str__(self):
        return f'{self.keyword} {self.num1} {self.num2}'

    def build(self):
        return f'{self.keyword} = "{self.num1} {self.num2}",'


def fullscreen(line:str):
    parts = line.strip().split(' ')
    if len(parts) != 1:
        fullscreen_type  = parts[1]
        if fullscreen_type == "1":
            return Var().set("fullscreen_mode", "maximize")
        if fullscreen_type == "2":
            return Var().set("fullscreen_mode", "fake")
    return Var().set("fullscreen", "true")

def workspace(line:str):
    workspace, mon = line.strip().split(' ')
    return Var().set("workspace", mon)

def suppressevent(line:str):
    key, action = [x.strip() for x in line.split(' ')]
    event = Var().set("suppress_event", action)
    return event

def monitor(line:str):
    _, name = line.strip().split(' ', 1)
    return Var().set("monitor", name)

def tile(line:str):
    return Var().set("float", "false")

def bordersize(line:str):
    _, n = line.strip().split(' ', 1)
    return Var().set("border_size", n)

def rounding(line:str):
    _, n = line.strip().split(' ', 1)
    return Var().set("rounding", n)

