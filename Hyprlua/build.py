from . import base_module, dataclass_module, inline_module
from .dataclass_module import File
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
        return multilines, new_lines

    def build(self, file:File):
        logger.debug(f'Building {file.name}')
        output_path = self.resolve_path(file)
        lines, multilines = self.collect_multilines(file.lines)

