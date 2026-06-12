from pathlib import Path
from .dataclass_module import *
from . import inline_module
from . import config_file
import logging
logger = logging.getLogger('HyprLua')

def lines_generator(lines:list):
    for line in lines:
        if line.strip() == '':
            yield EmptyLine()
        elif line.strip().startswith('#'):
            yield Comment().parse(line, None)
        else:
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

    def return_new_conf_obj(self, path:Path) -> config_file.ConfExtraFile:
        new_conf_file = self.conf_obj.conf_file / path
        return config_file.ConfExtraFile(new_conf_file)

    def start_parser(self):
        logger.info('Starting parser for {}'.format(self.conf_file))
        if not self.conf_file.exists():
            logger.error('Config file does not exist: {}'.format(self.conf_file))
            return None

        hyprland_file = File(name=self.conf_file.name, location=self.conf_file)
        return self.parse(hyprland_file)
        
    def parse(self, file:File):
        lines = file.location.read_text().split('\n')
        generator = lines_generator(lines)
        line = next(generator)

        while line is not None:
            logger.debug('Processing line: {}'.format(line))
            if isinstance(line, str):
                if line.__contains__('{'):
                    parsed_line = self._multiline_parse(line, generator)
                    file.add_line(parsed_line)
                    line = next(generator)
                    continue

                file.add_line(self._parse(line))
            else:
                file.add_line(line)
            line = next(generator)
        return file

    def _parse(self, line:str|list):

        for keyword, cls in self.parser_dir.items():
            if line.startswith(keyword):
                #logger.debug('Parsing line: {}'.format(line))
                new_cls = cls()
                new_cls.parse(line, self)
                return new_cls

        logger.error('No parser found for line: {}'.format(line))
        return Comment().parse(line, self)

    def _parse_lines(self, line:list):
        _line = line[0]

        for keyword, cls in self.parser_dir.items():
            if _line.startswith(keyword):
                #logger.debug('Parsing line: {}'.format(line))
                new_cls = cls()
                new_cls.parse(line, self)
                return new_cls

        logger.error('No parser found for lines:\n{}'.format(line))
        return Comment().parse(line, self)

    def _multiline_parse(self, line:str, generator):
        line_list = [line]

        while line is not None:
            line = next(generator)

            if isinstance(line, str):
                if line.__contains__('}'):
                    line_list.append(line)
                    break

                if line.__contains__('{'):
                    line_list.append(self._multiline_parse(line, generator))
                    continue
            line_list.append(line)

        if line is None:
            logger.error('Unexpected end of file while parsing multiline block')
            raise StopIteration('Unexpected end of file while parsing multiline block')
        return self._parse_lines(line_list)

    @staticmethod
    def var_inline_parse(line:str):
        line = line.split('=')[1].strip()
        _vars = line.split(',')
        _vars = [v.strip() for v in _vars]
        return _vars

    def _var_multiline_parse(self, line):
        for cls in self.inline_dir:
            if cls.check(line):
                new_cls = cls()
                return new_cls.parse(line, self)
        logger.error('No parser found for inline: {}'.format(line))
        return Comment().parse(line, self)

    def var_multiline_parse(self, lines:list[str | list]):
        _return_list = list()
        for line in lines[1:-1]:
            if isinstance(line, list):
                _return_list.append(self.var_multiline_parse(line))
                continue

            if isinstance(line, str):
                _return_list.append(self._var_multiline_parse(line))
                continue

            _return_list.append(line)
        return inline_module.Category().parse(_return_list, lines[0], self)

