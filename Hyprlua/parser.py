from pathlib import Path
from .dataclass_module import *
import logging
logger = logging.getLogger('HyprLua')

def lines_generator(lines:list):
    for line in lines:
        yield line.strip()
    yield None

class Parser:
    
    def __init__(self, conf_file:Path) -> None:
        self.conf_file = conf_file
        self.parser_dir = self.build_parser_dir()

    @staticmethod
    def build_parser_dir():
        _dicit = {}
        for cls in REGISTRY:
            _dicit[cls.keyword] = cls
        return _dicit

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
            if line=='':
                file.add_line(EmptyLine())
                line = next(generator)
                continue
            if line.__contains__('{'):
                generator, parsed_line = self._multiline_parse(line, generator)
                file.add_line(parsed_line)
                line = next(generator)
                continue

            logger.debug('Processing line: {}'.format(line))
            file.add_line(self._parse(line))
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
        return Comment(content='#'+line)

    def _parse_lines(self, line:list):
        _line = line[0]

        for keyword, cls in self.parser_dir.items():
            if _line.startswith(keyword):
                #logger.debug('Parsing line: {}'.format(line))
                new_cls = cls()
                new_cls.parse(line, self)
                return new_cls

        logger.error('No parser found for lines:\n{}'.format(line))
        comments = [Comment('#' + l) for l in line]
        return comments


    def _multiline_parse(self, line:str, generator):
        line_list = [line]

        while not line.__contains__('}'):
            line = next(generator)
            if line.__contains__('{'):
                line = self._multiline_parse(line, line_list)
            line_list.append(line)
            if line is None:
                logger.error('Unexpected end of file while parsing multiline block')
                raise StopIteration('Unexpected end of file while parsing multiline block')
        line_list.append(line)
        return generator, self._parse_lines(line_list)








    
        