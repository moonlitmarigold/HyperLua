import Hyprlua
from Hyprlua import parser, config_file, build
from Hyprlua.dataclass_module import Windowrule, Windowrulev2, Workspace
from Hyprlua.inline_module import Animation, Bezier
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


# --- Workspace rules ---

def test_workspace_parse_numeric():
    ws = Workspace().parse("workspace = 1, monitor:DP-1")
    assert ws.rules[0].var_name == "workspace"
    assert ws.rules[0].var_value == "1"

def test_workspace_parse_named():
    ws = Workspace().parse("workspace = name:coding, monitor:DP-1")
    assert ws.rules[0].var_name == "workspace"
    assert ws.rules[0].var_value == "name:coding"

def test_workspace_build_with_monitor():
    ws = Workspace().parse("workspace = 1, monitor:DP-1")
    assert ws.build() == 'hl.workspace_rule({ workspace = 1, monitor = "DP-1", })'

def test_workspace_build_named_with_default():
    ws = Workspace().parse("workspace = name:coding, monitor:DP-1, default:true, gaps_in:0")
    assert ws.build() == 'hl.workspace_rule({ workspace = "name:coding", monitor = "DP-1", default = true, gaps_in = 0, })'

def test_workspace_build_smart_gap_selector():
    ws = Workspace().parse("workspace = w[tv1], gaps_out:0, gaps_in:0")
    assert ws.build() == 'hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0, })'

def test_workspace_build_persistent():
    ws = Workspace().parse("workspace = 3, persistent:true")
    assert ws.build() == 'hl.workspace_rule({ workspace = 3, persistent = true, })'


# --- Windowrule (old single-line style) ---

def test_windowrule_parse_bool_action():
    wr = Windowrule().parse("windowrule = float, ^(pavucontrol)$")
    assert wr.action == "float"
    assert wr.match.match_type == "class"
    assert wr.match.match_value == "^(pavucontrol)$"

def test_windowrule_parse_value_action():
    wr = Windowrule().parse("windowrule = size 800 600, ^(pavucontrol)$")
    assert wr.action == "size 800 600"
    assert wr.match.match_value == "^(pavucontrol)$"

def test_windowrule_build_float():
    wr = Windowrule().parse("windowrule = float, ^(pavucontrol)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(pavucontrol)$" }, float = true, })'

def test_windowrule_build_noblur():
    wr = Windowrule().parse("windowrule = noblur, ^(firefox)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(firefox)$" }, no_blur = true, })'

def test_windowrule_build_nofocus():
    wr = Windowrule().parse("windowrule = nofocus, ^()$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^()$" }, no_focus = true, })'

def test_windowrule_build_pin():
    wr = Windowrule().parse("windowrule = pin, ^(stickynotes)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(stickynotes)$" }, pin = true, })'

def test_windowrule_build_size():
    wr = Windowrule().parse("windowrule = size 800 600, ^(pavucontrol)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(pavucontrol)$" }, size = "800 600", })'

def test_windowrule_build_move():
    wr = Windowrule().parse("windowrule = move 100 100, ^(myapp)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(myapp)$" }, move = "100 100", })'

def test_windowrule_build_workspace():
    wr = Windowrule().parse("windowrule = workspace 2, ^(firefox)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(firefox)$" }, workspace = 2, })'

def test_windowrule_build_opacity():
    wr = Windowrule().parse("windowrule = opacity 0.9, ^(kitty)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(kitty)$" }, opacity = { active = 0.9, }, })'

def test_windowrule_build_fullscreen():
    wr = Windowrule().parse("windowrule = fullscreen, ^(gamescope)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(gamescope)$" }, fullscreen = true, })'


# --- Windowrulev2 ---

def test_windowrulev2_build_float():
    wr = Windowrulev2().parse("windowrulev2 = float, class:^(xdg-desktop-portal-gtk)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(xdg-desktop-portal-gtk)$", }, float = true, })'

def test_windowrulev2_build_opacity_two_values():
    wr = Windowrulev2().parse("windowrulev2 = opacity 0.9 0.7, class:^(kitty)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(kitty)$", }, opacity = { active = 0.9, inactive = 0.7, }, })'

def test_windowrulev2_build_multi_filter():
    wr = Windowrulev2().parse("windowrulev2 = noblur, class:^(firefox)$,title:^(.*YouTube.*)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(firefox)$", title = "^(.*YouTube.*)$", }, no_blur = true, })'

def test_windowrulev2_build_suppress_event():
    wr = Windowrulev2().parse("windowrulev2 = suppressevent maximize, class:^(.*)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(.*)$", }, suppress_event = "maximize", })'

def test_windowrule_build_tile():
    wr = Windowrule().parse("windowrule = tile, ^(Spotify)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(Spotify)$" }, float = false, })'

def test_windowrulev2_build_monitor():
    wr = Windowrulev2().parse("windowrulev2 = monitor DP-2, class:^(discord)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(discord)$", }, monitor = "DP-2", })'

def test_windowrulev2_build_minsize():
    wr = Windowrulev2().parse("windowrulev2 = minsize 800 600, class:^(myapp)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(myapp)$", }, min_size = "800 600", })'

def test_windowrulev2_build_maxsize():
    wr = Windowrulev2().parse("windowrulev2 = maxsize 1920 1080, class:^(myapp)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(myapp)$", }, max_size = "1920 1080", })'

def test_windowrulev2_build_bordersize():
    wr = Windowrulev2().parse("windowrulev2 = bordersize 2, class:^(myapp)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(myapp)$", }, border_size = 2, })'

def test_windowrulev2_build_rounding():
    wr = Windowrulev2().parse("windowrulev2 = rounding 5, class:^(myapp)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(myapp)$", }, rounding = 5, })'

def test_windowrulev2_build_fullscreen_maximize():
    wr = Windowrulev2().parse("windowrulev2 = fullscreen 1, class:^(gamescope)$")
    assert wr.build() == 'hl.window_rule({ name = "windowrule0", match = { class = "^(gamescope)$", }, fullscreen_mode = "maximize", })'


# --- Animation ---

def test_animation_parse():
    anim = Animation().parse("animation = global, 1, 10, default")
    assert anim.animation_rule == "animation = global, 1, 10, default"

def test_animation_build_no_style():
    anim = Animation().parse("animation = global, 1, 10, default")
    assert anim.build() == 'hl.animation({ leaf = "global", enabled = true, speed = 10, bezier = "default" })'

def test_animation_build_with_style():
    anim = Animation().parse("animation = windowsIn, 1, 4.1, easeOutQuint, popin 87%")
    assert anim.build() == 'hl.animation({ leaf = "windowsIn", enabled = true, speed = 4.1, bezier = "easeOutQuint", style = "popin 87%" })'

def test_animation_build_disabled():
    anim = Animation().parse("animation = border, 0, 5.39, easeOutQuint")
    assert anim.build() == 'hl.animation({ leaf = "border", enabled = false, speed = 5.39, bezier = "easeOutQuint" })'


# --- Bezier ---

def test_bezier_parse():
    b = Bezier().parse("bezier = easeOutQuint, 0.23, 1, 0.32, 1")
    assert b.bezier == "bezier = easeOutQuint, 0.23, 1, 0.32, 1"

def test_bezier_build():
    b = Bezier().parse("bezier = easeOutQuint, 0.23, 1, 0.32, 1")
    assert b.build() == 'hl.curve("easeOutQuint", { type = "bezier", points = { {0.23, 1}, {0.32, 1} } })'

def test_bezier_build_linear():
    b = Bezier().parse("bezier = linear, 0, 0, 1, 1")
    assert b.build() == 'hl.curve("linear", { type = "bezier", points = { {0, 0}, {1, 1} } })'

def test_bezier_build_float_points():
    b = Bezier().parse("bezier = almostLinear, 0.5, 0.5, 0.75, 1")
    assert b.build() == 'hl.curve("almostLinear", { type = "bezier", points = { {0.5, 0.5}, {0.75, 1} } })'