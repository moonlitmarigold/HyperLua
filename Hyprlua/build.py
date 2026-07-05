from . import base_module, dataclass_module, inline_module
from .dataclass_module import File, ExecOnce, Exec
from .base_module import Line, MultiLine
from . import config_file
import logging
from .inline_module import Category
import os

logger = logging.getLogger('HyprLua')

class Builder:

    def __init__(self, input_conf, output_conf):
        self.input_conf:config_file.Conf|config_file.ConfExtraFile = input_conf
        self.output_conf:config_file.Conf|config_file.ConfExtraFile = output_conf

        self.windowrule = 1


    def resolve_path(self, file:File):
        diff = file.location.relative_to(self.input_conf.conf_dir)
        new_path =  self.output_conf.conf_dir / diff
        new_path.parent.mkdir(parents=True, exist_ok=True)

        if new_path.name == 'hyprland.conf':
            new_path = new_path.with_name('hypr')
        new_path = new_path.with_suffix('.lua')
        new_path.touch(exist_ok=True)
        logger.debug(f'Resolving {file.location} to {new_path}')
        return new_path

    def collect_multilines(self, lines:list):
        multilines = []
        new_lines = []
        for line in lines:
            if isinstance(line, MultiLine) and line.category_obj.category_name not in dataclass_module.HL_CONFIG_EXPECTIONS:
                multilines.append(line)
            else:
                new_lines.append(line)
        return new_lines, multilines

    def collect_animations(self, multilines):
        # The `animations {}` block is special: `enabled`/etc. are hl.config options,
        # but `bezier`/`animation` lines translate to top-level hl.curve()/hl.animation()
        # statements that must NOT live inside the hl.config({ animations = {} }) table.
        new_multilines = []
        animations = None
        for line in multilines:
            if line.category_obj is not None and line.category_obj.category_name == 'animations':
                animations = line
            else:
                new_multilines.append(line)
        return new_multilines, animations

    def build_animations(self, animations):
        inner = animations.category_obj.lines[1:-1]
        statement_lines = []  # hl.curve()/hl.animation() + surrounding comments -> top level
        config_lines = []     # plain options (enabled, ...) -> hl.config({ animations = {} })
        for line in inner:
            is_curve = isinstance(line, Line) and isinstance(
                line.pars_obj, (inline_module.Animation, inline_module.Bezier))
            if is_curve:
                statement_lines.append(line.reset_indent())
            elif isinstance(line, Line) and line.pars_obj is not None and not line.is_comment:
                config_lines.append(line.reset_indent().add_indent().add_indent())
            else:
                # comments / blank lines stay with the top-level curve section
                if isinstance(line, Line):
                    line.reset_indent()
                statement_lines.append(line)

        result = []
        if config_lines:
            result.append('hl.config({')
            result.append('    animations = {')
            result.extend(l.build() for l in config_lines)
            result.append('    },')
            result.append('})')
            result.append('')
        result.extend(l.build() for l in statement_lines)
        return '\n'.join(result)

    def collect_exec(self, lines):
        new_lines = []
        exec_lines = []
        for line in lines:
            if isinstance(line, Line) and (isinstance(line.pars_obj, ExecOnce) and not isinstance(line.pars_obj, Exec)):
                exec_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines, exec_lines

    def set_rule_numbers(self, lines):
        for line in lines:
            if isinstance(line, Line) and isinstance(line.pars_obj, dataclass_module.Windowrule):
                line.pars_obj.rule_number = self.windowrule
                self.windowrule += 1
        
        return lines

    def build(self, file:File):
        logger.debug(f'Building {file.name}')
        output_path = self.resolve_path(file)
        lines, multilines = self.collect_multilines(file.lines)
        multilines, animations = self.collect_animations(multilines)

        return_lines = list()
        return_lines.append('-- This Hyprland lua config is auto translated from the old Hyprlang')
        return_lines.append('')


        # Build all multilines at the top of the file
        if multilines:
            return_lines.append('-- Hyprland variables')
            return_lines.append('')
            for l in multilines:
                l.add_indent()
            return_lines.append('hl.config({')
            return_lines.append('\n'.join([l.build() for l in multilines]))
            return_lines.append('}, true)')
            return_lines.append('')

        # Animations translate to top-level hl.curve()/hl.animation() statements,
        # with any plain options kept in their own hl.config({ animations = {} }) call.
        if animations is not None:
            return_lines.append('-- Hyprland animations')
            return_lines.append('')
            return_lines.append(self.build_animations(animations))
            return_lines.append('')

        # Build all execs
        lines, exec_lines = self.collect_exec(lines)
        if exec_lines:
            return_lines.append('-- Hyprland start execs')
            return_lines.append('')
            for l in exec_lines:
                l.add_indent()
            return_lines.append('hl.on("hyprland.start", function()')
            return_lines.append('\n'.join([l.build() for l in exec_lines]))
            return_lines.append('end)')
            return_lines.append('')

        # Set rule number to have syntax like 'windowrule1', 'windowrule2', etc.
        lines = self.set_rule_numbers(lines)

        # Build the rest of the file
        for line in lines:
            if isinstance(line, File):
                return_lines.append(line.build(self))
            else:
                return_lines.append(line.build())

        full_text = '\n'.join(return_lines)
        output_path.write_text(full_text)
        return full_text

