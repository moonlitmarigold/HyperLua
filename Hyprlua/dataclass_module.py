import dataclasses
from pathlib import Path
from .base_module import *
from . import inline_module
from . import config_file
import copy
from typing import Callable, Dict

REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally


@register
@dataclasses.dataclass
class File(Base):
    conf_obj:config_file.Conf | config_file.ConfExtraFile = None
    keyword: ClassVar[str] = 'source'
    lines:list = dataclasses.field(default_factory=list)
    rel_location:str = ''

    @property
    def name(self):
        return self.location.name

    @property
    def location(self):
        return self.conf_obj.conf_file

    @property
    def dir(self):
        return self.conf_obj.conf_dir

    def parse(self, line:str, parser_class, parent_file):
        self.rel_location = line.split('=')[1].strip()
        location = Path(line.split('=')[1].strip()).expanduser()
        self.conf_obj = config_file.ConfExtraFile(parent_file.conf_obj.conf_dir / location)
        parser_class.parse(self)
        return self

    def add_line(self, line_obj:type(Base)):
        self.lines.append(line_obj)

    def __str__(self):
        return str_lines(self.lines)

    def build(self, builder_obj):
        builder_obj.build(self)
        return f'require("{self.rel_location}")'

@register
@dataclasses.dataclass
class Monitor(Base):
    keyword: ClassVar[str] = 'monitor'

    name= ''
    resolution= ''
    position= ''
    scale= ''

    def parse(self, line:str):
        self._parse(line)
        self.name, self.resolution, self.position, self.scale = self.var_inline_parse(line)
        return self

    def __str__(self):
        return f'monitor = {self.name}, {self.resolution}, {self.position}, {self.scale}'

    def build(self):
        _list = (
            f'output = {self.return_var_value(self.name)}',
            f'mode = {self.return_var_value(self.resolution)}',
            f'position = {self.return_var_value(self.position)}',
            f'scale = {self.return_var_value(self.scale)}',
        )
        return f'hl.monitor({{ {', '.join(_list) }, }})'

@register
@dataclasses.dataclass
class Env(Base):

    keyword: ClassVar[str] = 'env'
    var_name = ''
    var_value = ''

    def parse(self, line:str):
        self._parse(line)
        self.var_name, self.var_value = self.var_inline_parse(line)
        return self

    def __str__(self):
        return f'env = {self.var_name},{self.var_value}'

    def build(self):
        return f'hl.env("{self.var_name}", "{self.var_value}")'

@register
@dataclasses.dataclass
class Var(Base):

    keyword: ClassVar[str] = '$'
    var_name = ''
    var_value = ''

    def parse(self, line:str):
        _vars = line.split('=')
        self.var_name, self.var_value = _vars[0].strip()[1:], _vars[1].strip()
        return self

    def __str__(self):
        return f'${self.var_name} = {self.var_value}'

    def build(self):
        return f'local {self.var_name} = {self.return_var_value(self.var_value)}'

@register
@dataclasses.dataclass
class ExecOnce(Base):
    keyword: ClassVar[str] = 'exec-once'
    start_script = ''

    def parse(self, line:str):
        self.start_script = line.split('=')[1].strip()
        return self

    def __str__(self):
        return f'{self.keyword} = {self.start_script}'

    def build(self):
        return f'hl.exec_cmd("{self.start_script}")'

@register
@dataclasses.dataclass
class Exec(ExecOnce):
    keyword: ClassVar[str] = 'exec'

@register
@dataclasses.dataclass
class Permission(Base):
    keyword: ClassVar[str] = 'permission'
    permission_prg = ''
    permission_type = ''
    permission_allow = ''

    def parse(self, line:str):
        self.permission_prg, self.permission_type, self.permission_allow =  [l.strip() for l in line.split('=')[1].strip().split(',')]
        return self

    def __str__(self):
        return f'permission = {self.permission_prg}, {self.permission_type}, {self.permission_allow}'

    def build(self):
        _return = (
            self.return_var_value(self.permission_prg),
            self.return_var_value(self.permission_type),
            self.return_var_value(self.permission_allow),
        )
        return f'hl.permission({', '.join(_return)})'

@register
@dataclasses.dataclass
class Workspace(Base):

    keyword: ClassVar[str] = 'workspace'
    rules:list = dataclasses.field(default_factory=lambda: [])

    def parse(self, line:str):
        keyword, value = [x.strip() for x in line.split("=", 1)]

        for i, token in enumerate([x.strip() for x in value.split(",") if x.strip()]):
            if ":" not in token and i == 0:
                _var = inline_module.Var()
                _var.var_name = 'workspace'
                _var.var_value = token
                self.rules.append(_var)
                continue

            k, v = [x.strip() for x in token.split(":", 1)]
            _var = inline_module.Var()
            if k == 'name':
                _var.var_name = 'workspace'
                _var.var_value = token
                self.rules.append(_var)
                continue

            _var.var_name = k
            _var.var_value = v
            self.rules.append(_var)

        return self

    def __str__(self):
        values = [str(x) for x in self.rules]
        str_values = ', '.join(values).replace(' = ', ':')
        return f'workspace = {str_values}'

    def build(self):
        return f'hl.workspace_rule({{ {' '.join([x.build() for x in self.rules])} }})'


@register
@dataclasses.dataclass
class Windowrule(Base):
    keyword: ClassVar[str] = 'windowrule '
    action = ''
    match:inline_module.Match = None
    bool_rules = {
        "float": "float",
        "fakefullscreen": "fake_fullscreen",
        "pin": "pin",
        "noblur": "no_blur",
        "noanim": "no_anim",
        "noborder": "no_border",
        "noshadow": "no_shadow",
        "nofocus": "no_focus",
        "nomaxsize": "no_max_size",
        "stayfocused": "stay_focused",
        "dimaround": "dim_around",
        "keepaspectratio": "keep_aspect_ratio",
        "decorate": "decorate",
        "renderunfocused": "render_unfocused",
        "center": "center",
    }

    rule_number = 0

    translation: Dict[str, Callable] = dataclasses.field(default_factory=lambda: {
        "opacity": inline_module.Opacity().parse,
        "fullscreen": inline_module.fullscreen,
        "size": inline_module.Size().parse,
        "move": inline_module.Size().set_key('move').parse,
        "minsize": inline_module.Size().set_key('min_size').parse,
        "maxsize": inline_module.Size().set_key('max_size').parse,
        "workspace": inline_module.workspace,
        "monitor": inline_module.monitor,
        "tile": inline_module.tile,
        "bordersize": inline_module.bordersize,
        "rounding": inline_module.rounding,
        "suppressevent": inline_module.suppressevent,
        "bordercolor": inline_module.BorderColor().parse,
    })

    def parse(self, line: str):
        keyword, value = [x.strip() for x in line.split("=", 1)]
        action, regex = [x.strip() for x in value.split(",", 1)]
        self.action = action
        _match = inline_module.Match()
        _match.match_type = 'class'
        _match.match_value = regex
        self.match = _match
        return self

    def __str__(self):
        return f'windowrule = {self.action}, {str(self.match)}'

    def build(self):
        options = list()
        options.append(f'name = "windowrule{self.rule_number}",')
        options.append(self.match.build())
        options.append(self._action())
        return 'hl.window_rule({ ' + ' '.join(options) + ' })'

    def _action(self):
        _action = self.action.strip().split(' ')[0].strip()
        logger.debug(f'action = {self.action}')
        if _action in self.bool_rules:
            return f'{self.bool_rules[_action]} = true,'
        if _action == 'title':
            return 'float = true,'
        if _action in self.translation.keys():
            return self.translation[_action](self.action).build()
        return self.action

# windowrulev2

@register
@dataclasses.dataclass
class Windowrulev2(Windowrule):
    keyword: ClassVar[str] = 'windowrulev2'
    multi_match:list = dataclasses.field(default_factory=lambda: [])


    def parse(self, line: str):
        #"windowrulev2 = noblur, class:^(firefox)$,title:^(.*YouTube.*)$"
        keyword, value = [x.strip() for x in line.split("=", 1)]
        parts = [x.strip() for x in value.split(",")]
        self.action = parts[0]
        for _match in parts[1:]:
            type_match, regex = [x.strip() for x in _match.split(":", 1)]
            self.multi_match.append(inline_module.Var().set(type_match, regex))
        return self

    def __str__(self):
        _l = list()
        _l.append(self.action)
        _l.extend([f'{x.var_name}:{x.var_value}' for x in self.multi_match])
        return 'windowrulev2 = ' + ', '.join(_l)

    def build(self):
        options = list()
        options.append(f'name = "windowrule{self.rule_number}",')
        options.append(self._match())
        options.append(self._action())
        return 'hl.window_rule({ ' + ' '.join(options) + ' })'

    def _match(self):
        return 'match = { ' + ' '.join([x.build() for x in self.multi_match]) + ' },'

CATEGORIES = (
    'windowrule', 'animations', 'general', 'decoration', 'input', 'gestures',
    'group', 'misc', 'binds', 'xwayland', 'opengl', 'render', 'debug', 'dwindle',
    'master', 'device', 'plugin', 'ecosystem'
)

HL_CONFIG_EXPECTIONS = (
    'gestures', 'windowrule',
)

