import Hyprlua
from Hyprlua import parser, config_file
from pathlib import Path

def test_parser():
    config_path = Path(__file__).parent
    print(config_path)

    _parser = parser.Parser(config_file.Conf(config_path))
    result = _parser.start_parser()
    print(result)
    assert True