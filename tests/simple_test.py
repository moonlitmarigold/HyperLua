import Hyprlua
from Hyprlua import parser, config_file, build
from pathlib import Path


def test_parser():
    config_path = Path(__file__).parent
    print(config_path)

    _parser = parser.Parser(config_file.Conf(config_path))
    result = _parser.start_parser()
    print(result)
    assert True

def test_builder():
    config_path = Path(__file__).parent
    print(config_path)
    output_path = Path(__file__).parent / "test_lua" / "test.lua"
    print(output_path)

    _parser = parser.Parser(config_file.Conf(config_path))
    _builder = build.Builder(config_file.Conf(config_path), config_file.ConfExtraFile(output_path))
    result = _parser.start_parser()
    result = _builder.build(result)
    print(result)