from pathlib import Path
from dataclass_module import *
import logging
logger = logging.getLogger('HyprLua')

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
        class_conf_file = File(name="Hyprland Config File", )
        return self.parse(self.conf_file)
        
    def parse(self, file):
        lines = self.conf_file.read_text().split('\n')
        for line in lines:
            line = line.strip()
            if not line:


    
        