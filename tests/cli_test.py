import Hyprlua
from Hyprlua import __main__ as m

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_conf():
    """Return a mock Conf object with a predictable conf_dir."""
    conf = MagicMock()
    conf.conf_dir = "/home/user/.config/hypr"
    return conf


# ---------------------------------------------------------------------------
# parse_arguments
# ---------------------------------------------------------------------------

class TestParseArguments:
    def test_defaults(self):
        """No arguments → config_path and output_path are None, help is False."""
        with patch("sys.argv", ["hyprlua"]):
            from Hyprlua import __main__ as m
            args = m.parse_arguments()
        assert args.config_path is None
        assert args.output_path is None
        assert args.help is False

    def test_config_short_flag(self):
        with patch("sys.argv", ["hyprlua", "-c", "/custom/path"]):
            from Hyprlua import __main__ as m
            args = m.parse_arguments()
        assert args.config_path == "/custom/path"

    def test_config_long_flag(self):
        with patch("sys.argv", ["hyprlua", "--config", "/another/path"]):
            from Hyprlua import __main__ as m
            args = m.parse_arguments()
        assert args.config_path == "/another/path"

    def test_output_flag(self):
        with patch("sys.argv", ["hyprlua", "-o", "/tmp/out.lua"]):
            from Hyprlua import __main__ as m
            args = m.parse_arguments()
        assert args.output_path == "/tmp/out.lua"

    def test_help_flag(self):
        with patch("sys.argv", ["hyprlua", "--help"]):
            from Hyprlua import __main__ as m
            args = m.parse_arguments()
        assert args.help is True

    def test_version_flag_exits(self):
        """--version should trigger SystemExit (argparse behaviour)."""
        with patch("sys.argv", ["hyprlua", "--version"]):
            from Hyprlua import __main__ as m
            with pytest.raises(SystemExit):
                m.parse_arguments()


# ---------------------------------------------------------------------------
# show_help
# ---------------------------------------------------------------------------

class TestShowHelp:
    def test_help_output_contains_usage(self, capsys):
        from Hyprlua import __main__ as m
        m.show_help()
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
        assert "HyprLua" in captured.out

    def test_help_mentions_config_flag(self, capsys):
        from Hyprlua import __main__ as m
        m.show_help()
        assert "--config" in capsys.readouterr().out

    def test_help_mentions_output_flag(self, capsys):
        from Hyprlua import __main__ as m
        m.show_help()
        assert "--output" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# get_conf_dir
# ---------------------------------------------------------------------------

class TestGetConfDir:
    def test_uses_provided_path(self, mock_conf):
        with patch("main.config_file.conf", return_value=mock_conf) as mock_fn:
            from Hyprlua import __main__ as m
            result = m.get_conf_dir("/custom/config")
        mock_fn.assert_called_once_with("/custom/config")
        assert result == mock_conf

    def test_uses_default_when_no_path(self, mock_conf):
        with patch("main.config_file.conf", return_value=mock_conf) as mock_fn:
            from Hyprlua import __main__ as m
            result = m.get_conf_dir()
        mock_fn.assert_called_once_with()
        assert result == mock_conf


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_shows_help_when_flag_set(self, capsys):
        with patch("sys.argv", ["hyprlua", "--help"]):
            from Hyprlua import __main__ as m
            m.main()
        assert "HyprLua" in capsys.readouterr().out

    def test_main_prints_config_dir(self, mock_conf, capsys):
        with patch("sys.argv", ["hyprlua"]):
            with patch("main.config_file.Conf", return_value=mock_conf):
                from Hyprlua import __main__ as m
                m.main()
        assert "/home/user/.config/hypr" in capsys.readouterr().out

    def test_main_passes_config_path_to_conf(self, mock_conf):
        with patch("sys.argv", ["hyprlua", "-c", "/my/config"]):
            with patch("main.config_file.Conf", return_value=mock_conf) as mock_cls:
                from Hyprlua import __main__ as m
                m.main()
        mock_cls.assert_called_once_with("/my/config")

    def test_main_passes_none_when_no_config_arg(self, mock_conf):
        with patch("sys.argv", ["hyprlua"]):
            with patch("main.config_file.Conf", return_value=mock_conf) as mock_cls:
                from Hyprlua import __main__ as m
                m.main()
        mock_cls.assert_called_once_with(None)