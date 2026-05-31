from pathlib import Path

class Parser:
    
    def __init__(self, conf_file:Path) -> None:
        self.conf_file = conf_file
        
    def parse(self):
        lines = self.conf_file.read_text().split('\n')
        for line in lines:
            print(line)
    
        