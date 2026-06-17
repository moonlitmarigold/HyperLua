from pathlib import Path
from .dataclass_module import *
from . import inline_module
from . import config_file
import logging

from .inline_module import Category

logger = logging.getLogger('HyprLua')

def lines_generator(lines:list):
    for line in lines:
        yield line
    yield None

class Parser:
    
    def __init__(self, conf_obj:config_file.Conf|config_file.ConfExtraFile) -> None:
        self.conf_obj = conf_obj
        self.conf_file = conf_obj.conf_file
        self.parser_dir = self.build_parser_dir()
        self.inline_dir = self.build_inline_dir()

    @staticmethod
    def build_parser_dir():
        _dicit = {}
        for cls in REGISTRY:
            _dicit[cls.keyword] = cls
        return _dicit

    @staticmethod
    def build_inline_dir():
        _list = list()
        return inline_module.REGISTRY

    @staticmethod
    def pre_parse(lines:list):
        def _parse(_line):
            _line = _line.strip()
            if _line == '':
                return EmptyLine()
            elif _line.startswith('#'):
                return Line(_line, is_comment=True)
            else:
                return line

        def _multiline(_line:str, _generator):
            if not _line.__contains__('{'):
                return Line(_line)
            line_list = [_parse(_line)]

            while _line is not None:
                _line = next(generator)

                if _line.__contains__('}'):
                    line_list.append(line)
                    break

                if _line.__contains__('{'):
                    line_list.append(_multiline(_line, _generator))
                    continue
                line_list.append(_parse(_line))
            return MultiLine(line_list)

        _lines = list()
        generator = lines_generator(lines)
        line = next(generator)

        while line is not None:
            line = _parse(line)
            if isinstance(line, str):
                _lines.append(_multiline(line, generator))
            else:
                _lines.append(line)
            line = next(generator)
        return _lines


    def start_parser(self):
        logger.info('Starting parser for {}'.format(self.conf_file))
        if not self.conf_file.exists():
            logger.error('Config file does not exist: {}'.format(self.conf_file))
            return None

        hyprland_file = File(name=self.conf_file.name, conf_obj=self.conf_obj)
        return self.parse(hyprland_file)
        
    def parse(self, file:File):
        lines = file.location.read_text().split('\n')
        lines = self.pre_parse(lines)
        generator = lines_generator(lines)
        line = next(generator)

        while line is not None:
            logger.debug('Processing line: {}'.format(line))

            if isinstance(line, Line) and not line.is_comment:
                if line.startswith('source'):
                    new_file = File().parse(line, self, file)
                    file.add_line(new_file)
                    line = next(generator)
                    continue

                file.add_line(self._parse(line))
                continue

            if isinstance(line, MultiLine):
                file.add_line(self._multiline_parse(line))

            file.add_line(line)
            line = next(generator)
        return file

    def _parse(self, line:Line):

        for keyword, cls in self.parser_dir.items():
            if line.startswith(keyword):
                return line.set_pars_obj(cls)

        logger.error('No parser found for line: {}'.format(line))
        return line.set_commented()

    def _multiline_parse(self, multiline:MultiLine, sub_category = False):

        category_name = multiline.lines[0]
        _return_list = list()
        for line in multiline.lines[1:-1]:
            if isinstance(line, Line) and not line.is_comment:
                _return_list.append(self._inline_parse(line))
                continue

            if isinstance(line, MultiLine):
                _return_list.append(self._multiline_parse(line, True))
                continue

            _return_list.append(line)
        category = Category(category_name, _return_list)
        if not sub_category:
            if category_name not in CATEGORIES:
                logger.error('No parser found for category: {}'.format(category_name))
                multiline.set_commented()

        return multiline.set_category_obj(category)

    def _inline_parse(self, line:Line):
        for cls in self.inline_dir:
            if cls.check(line):
                return line.set_pars_obj(cls)
        logger.error('No parser found for inline: {}'.format(line))
        return line.set_commented()

