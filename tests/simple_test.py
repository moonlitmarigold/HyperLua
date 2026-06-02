import Hyprlua
from Hyprlua import parser
from pathlib import Path

def test_parser():
    config_path = Path(__file__).parent / "hyprland.conf"

    _parser = parser.Parser(config_path)
    result = _parser.start_parser()
    print(result)
    assert True