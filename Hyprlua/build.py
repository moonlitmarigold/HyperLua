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
            if isinstance(line, MultiLine):
                multilines.append(line)
            else:
                new_lines.append(line)
        return new_lines, multilines

    def collect_exec(self, lines):
        new_lines = []
        exec_lines = []
        for line in lines:
            if isinstance(line, Line) and (isinstance(line.pars_obj, ExecOnce) or isinstance(line.pars_obj, Exec)):
                exec_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines, exec_lines

    def build(self, file:File):
        logger.debug(f'Building {file.name}')
        output_path = self.resolve_path(file)
        lines, multilines = self.collect_multilines(file.lines)

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


        return '\n'.join(return_lines)

