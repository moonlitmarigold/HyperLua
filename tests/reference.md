# Hyprland hyprlang Configuration Reference (pre-0.55 / `.conf` syntax)

> **Note:** This covers the **hyprlang** (`.conf`) configuration syntax used in Hyprland **up to and including version 0.54**.  
> Starting with **0.55**, Hyprland uses Lua (`hyprland.lua`) and hyprlang is deprecated.  
> Config file location: `~/.config/hypr/hyprland.conf`

---

## 1. Syntax Basics

```ini
# This is a comment
## This is a literal # (escaped), NOT a comment — produces a single #

# Key-value assignment
option = value

# Category (block) syntax
category {
    option = value
    sub_category {
        option = value
    }
}

# Inline category syntax (used by hyprctl keyword)
category:option = value

# Source another file
source = ~/.config/hypr/other.conf

# Variables (user-defined)
$myVar = value
option = $myVar

# Arithmetic on variables (hyprlang >= 0.6.3)
$a = 10
$b = 5
option = {{$a + $b}}   # evaluates to 15
# Supported: +, -, *, /  (two operands at a time)

# Conditional blocks (hyprlang >= 0.6.4)
# hyprlang if $MY_ENV_VAR
option = value_if_true
# hyprlang endif

# Suppress missing option/keyword errors (useful for plugins)
# hyprlang noerror true
bind = MOD, KEY, somePluginDispatcher, args
# hyprlang noerror false
```

**Value types:**
| Type | Example |
|---|---|
| int | `1`, `42` |
| float | `1.0`, `0.5` |
| bool | `true` / `false` or `1` / `0` |
| color | `rgb(rrggbb)`, `rgba(rrggbbaa)` |
| string | `hello`, `^(regex)$` |
| vec2 | `100 200` |
| gradient | `rgba(ff0000ff) rgba(0000ffff) 45deg` |

---

## 2. Monitors

```ini
# monitor = NAME, RESOLUTION@REFRESHRATE, POSITION, SCALE
monitor = DP-1, 1920x1080@144, 0x0, 1
monitor = HDMI-A-1, 2560x1440@60, 1920x0, 1.5
monitor = eDP-1, preferred, auto, 1          # laptop screen, auto-position
monitor = ,preferred,auto,1                   # catch-all / unknown monitors
monitor = DP-2, disable                       # disable a monitor

# Additional monitor options
monitor = DP-1, 1920x1080@144, 0x0, 1, transform, 1     # 90° rotation
monitor = DP-1, 1920x1080@144, 0x0, 1, bitdepth, 10     # 10-bit color
monitor = DP-1, 1920x1080@144, 0x0, 1, mirror, HDMI-A-1 # mirror another

# Position keywords: auto, auto-left, auto-right, auto-up, auto-down
```

---

## 3. Variables / Options

All options are set inside named category blocks. Multiple levels of nesting are supported.

### 3.1 `general`

```ini
general {
    gaps_in = 5               # gap between windows (inner)
    gaps_out = 10             # gap between windows and monitor edges (outer)
    border_size = 2           # window border thickness in pixels
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.inactive_border = rgba(595959aa)
    no_border_on_floating = false
    layout = dwindle          # dwindle | master
    allow_tearing = false     # allow screen tearing (for low-latency gaming)
    resize_on_border = false  # drag border to resize windows
    extend_border_grab_area = 15
    hover_icon_on_border = true
    snap {
        enabled = false
        window_gap = 10
        monitor_gap = 10
    }
}
```

### 3.2 `decoration`

```ini
decoration {
    rounding = 10             # corner rounding in pixels
    active_opacity = 1.0
    inactive_opacity = 1.0
    fullscreen_opacity = 1.0
    drop_shadow = true
    shadow_range = 4
    shadow_render_power = 3   # 1-4
    col.shadow = rgba(1a1a1aee)
    col.shadow_inactive = unset
    shadow_offset = 0 0
    shadow_scale = 1.0
    dim_inactive = false
    dim_strength = 0.5        # 0.0 - 1.0
    dim_special = 0.2
    dim_around = 0.4
    screen_shader =           # path to a GLSL fragment shader

    blur {
        enabled = true
        size = 3              # blur kernel size
        passes = 1            # number of passes (increase for larger size)
        ignore_opacity = false
        new_optimizations = on
        xray = false
        noise = 0.0117
        contrast = 0.8916
        brightness = 0.8172
        vibrancy = 0.1696
        vibrancy_darkness = 0.0
        special = false
        popups = false
        popups_ignorealpha = 0.2
    }
}
```

### 3.3 `animations`

```ini
animations {
    enabled = true
    first_launch_animation = true

    # bezier = NAME, X0, Y0, X1, Y1
    bezier = myBezier, 0.05, 0.9, 0.1, 1.05
    bezier = linear, 0.0, 0.0, 1.0, 1.0
    bezier = easeOut, 0.0, 0.0, 0.2, 1.0

    # animation = EVENT, ONOFF, SPEED, CURVE [, STYLE]
    animation = windows, 1, 7, myBezier
    animation = windowsOut, 1, 7, default, popin 80%
    animation = border, 1, 10, default
    animation = borderangle, 1, 8, default
    animation = fade, 1, 7, default
    animation = workspaces, 1, 6, default
    animation = specialWorkspace, 1, 6, default, slidevert
}
```

**Animation events tree:**
```
global
└── windows          (styles: slide, popin, gnomed)
    ├── windowsIn    (window open)
    ├── windowsOut   (window close)
    └── windowsMove  (moving/dragging/resizing)
fade
├── fadeIn
├── fadeOut
├── fadeSwitch
├── fadeShadow
├── fadeDim
└── fadeLayers
border
└── borderangle
workspaces           (styles: slide, slidevert, fade, pop, name)
├── specialWorkspace
└── ...
layers               (styles: slide, popin, fade)
```

### 3.4 `input`

```ini
input {
    kb_model =
    kb_layout = us
    kb_variant =
    kb_options =
    kb_rules =
    kb_file =                   # path to XKB file
    numlock_by_default = false
    resolve_binds_by_sym = false
    repeat_rate = 25            # key repeat rate (keys/sec)
    repeat_delay = 600          # delay before repeat starts (ms)
    sensitivity = 0.0           # mouse sensitivity (-1.0 to 1.0)
    accel_profile = adaptive    # flat | adaptive | custom
    force_no_accel = false
    left_handed = false
    scroll_points =             # for custom accel profile
    scroll_method = 2fg         # no_scroll | 2fg | edge | on_button_down
    scroll_button = 0
    scroll_button_lock = 0
    scroll_factor = 1.0
    natural_scroll = false
    follow_mouse = 1            # 0=disabled, 1=full, 2=loose, 3=loose+click
    mouse_refocus = true
    float_switch_override_focus = 1
    special_fallthrough = false
    off_window_axis_events = 1

    touchpad {
        disable_while_typing = true
        natural_scroll = false
        scroll_factor = 1.0
        middle_button_emulation = false
        tap_button_map = lrm     # lrm | lmr
        clickfinger_behavior = false
        tap-to-click = true
        drag_lock = false
        tap-and-drag = false
    }

    touchscreen {
        output =
        transform = 0
    }
}
```

### 3.5 `gestures`

```ini
gestures {
    workspace_swipe = false
    workspace_swipe_fingers = 3
    workspace_swipe_min_fingers = false
    workspace_swipe_distance = 300
    workspace_swipe_touch = false
    workspace_swipe_invert = true
    workspace_swipe_min_speed_to_force = 30
    workspace_swipe_cancel_ratio = 0.5
    workspace_swipe_create_new = true
    workspace_swipe_direction_lock = true
    workspace_swipe_direction_lock_threshold = 10
    workspace_swipe_forever = false
    workspace_swipe_use_r = false
}
```

### 3.6 `group`

```ini
group {
    insert_after_current = true
    focus_removed_window = true
    col.border_active = 0x66ffff00
    col.border_inactive = 0x66777700
    col.border_locked_active = 0x66ff5500
    col.border_locked_inactive = 0x66775500

    groupbar {
        enabled = true
        font_family = sans
        font_size = 8
        gradients = true
        height = 14
        priority = 3
        render_titles = true
        scrolling = true
        text_color = 0xffffffff
        col.active = 0x66ffff00
        col.inactive = 0x66777700
        col.locked_active = 0x66ff5500
        col.locked_inactive = 0x66775500
    }
}
```

### 3.7 `misc`

```ini
misc {
    disable_hyprland_logo = false
    disable_splash_rendering = false
    col.splash = 0xffffffff
    splash_font_family =
    force_default_wallpaper = -1    # 0, 1, 2 — or -1 to keep last seen
    vfr = true                       # variable framerates (saves power)
    vrr = 0                          # variable refresh rate: 0=off, 1=on, 2=fullscreen only
    mouse_move_enables_dpms = false
    key_press_enables_dpms = false
    always_follow_on_dnd = true
    layers_hog_keyboard_focus = true
    animate_manual_resizes = false
    animate_mouse_windowdragging = false
    disable_autoreload = false
    enable_swallow = false
    swallow_regex =
    swallow_exception_regex =
    focus_on_activate = false
    mouse_move_focuses_monitor = true
    render_ahead_of_time = false
    render_ahead_safezone = 1
    allow_session_lock_restore = false
    background_color = 0x111111
    close_special_on_empty = true
    new_window_takes_over_fullscreen = 0
    exit_window_retains_fullscreen = false
    initial_workspace_tracking = 1
    middle_click_paste = true
    render_unfocused_fps = 15
    disable_xdg_env_checks = false
}
```

### 3.8 `binds` (options category)

```ini
binds {
    pass_mouse_when_bound = false
    scroll_event_delay = 300
    workspace_back_and_forth = false
    allow_workspace_cycles = false
    workspace_center_on = 0
    focus_preferred_method = 0
    ignore_group_lock = false
    movefocus_cycles_fullscreen = false
    disable_keybind_grabbing = false
    window_direction_monitor_fallback = true
}
```

### 3.9 `xwayland`

```ini
xwayland {
    use_nearest_neighbor = true
    force_zero_scaling = false
}
```

### 3.10 `opengl`

```ini
opengl {
    nvidia_anti_flicker = true
    force_introspection = 2   # 0=off, 1=on, 2=force
}
```

### 3.11 `render`

```ini
render {
    explicit_sync = 2         # 0=off, 1=on, 2=auto
    explicit_sync_kms = 2
    direct_scanout = false
}
```

### 3.12 `cursor`

```ini
cursor {
    no_hardware_cursors = false
    hotspot_padding = 1
    inactive_timeout = 0     # seconds before hiding cursor; 0 = never
    no_break_fs_vrr = false
    min_refresh_rate = 24
    clickable_region = 0
    enable_hyprcursor = true
    sync_gsettings_theme = true
    warp_on_change_workspace = false
    persistent_warps = false
    warp_back_after_non_mouse_input = false
    zoom_factor = 1.0
    zoom_rigid = false
    use_cpu_buffer = 0
    hide_on_key_press = false
    hide_on_touch = true
}
```

### 3.13 `debug`

```ini
debug {
    overlay = false
    damage_blink = false
    disable_logs = true
    disable_time = true
    damage_tracking = 2
    enable_stdout_logs = false
    manual_crash = 0
    suppress_errors = false
    watchdog_timeout = 5
    disable_scale_checks = false
    error_limit = 5
    error_position = 0
    colored_stdout_logs = true
}
```

---

## 4. Layouts

### 4.1 Dwindle

```ini
dwindle {
    pseudotile = false         # enable pseudo-tiling mode
    force_split = 0            # 0=follow mouse, 1=always left/top, 2=always right/bottom
    preserve_split = false
    smart_split = false
    smart_resizing = true
    permanent_direction_override = false
    special_scale_factor = 0.8
    split_width_multiplier = 1.0
    no_gaps_when_only = 0      # 0=off, 1=no gaps if 1 window, 2=+no border
    use_active_for_splits = true
    default_split_ratio = 1.0  # 0.1 - 1.9
    split_bias = 0             # 0=none, 1=left/top, 2=right/bottom
}
```

### 4.2 Master

```ini
master {
    allow_small_split = false
    special_scale_factor = 0.8
    mfact = 0.55               # master area size ratio (0.05 - 0.95)
    new_status = slave         # master | slave | inherit
    new_on_top = false
    new_on_active = none       # none | before | after
    no_gaps_when_only = 0
    orientation = left         # left | right | top | bottom | center
    inherit_fullscreen = true
    always_center_master = false
    smart_resizing = true
    drop_at_cursor = true
}
```

---

## 5. Keywords (Special Directives)

### 5.1 `exec` / `exec-once`

```ini
exec-once = waybar
exec-once = swaync
exec-once = swww-daemon
exec = ~/.config/hypr/reload_script.sh   # runs on every config reload
```

### 5.2 `env`

```ini
env = XCURSOR_SIZE,24
env = HYPRCURSOR_SIZE,24
env = QT_QPA_PLATFORM,wayland
env = GDK_BACKEND,wayland,x11
env = MOZ_ENABLE_WAYLAND,1
```

### 5.3 `bind` / `bindm` / `binde` / `bindr` / `bindl` / `bindn` / `bindp`

```ini
# bind = MODS, KEY, DISPATCHER, [PARAMS]
bind = SUPER, Q, killactive
bind = SUPER, RETURN, exec, kitty
bind = SUPER, F, fullscreen
bind = SUPER SHIFT, F, fullscreen, 1

# Modifier keys: SHIFT, CTRL (or CONTROL), ALT, SUPER (or WIN/LOGO), META, HYPER
# Combine: SUPER SHIFT, SUPER CTRL ALT, etc.
# No modifier: leave empty — , KEY, ...

# Mouse buttons: mouse:272 (LMB), mouse:273 (RMB), mouse:274 (MMB)
bindm = SUPER, mouse:272, movewindow
bindm = SUPER, mouse:273, resizewindow

# Bind flags (can combine):
# e = repeat while held (binde)
# r = release trigger (bindr)
# l = works when screen locked (bindl)
# n = non-consuming (bindn) — does not consume the key event
# p = passthrough (bindp) — pass to window even if bound
# m = mouse bind (bindm)
# t = transparent — do not consume event if no window accepts
# i = ignore mods when locked
# s = special workspace

# Long-form flag syntax
bind = SUPER, Q, killactive        # same as flags: none
binde = SUPER, right, resizeactive, 10 0
bindr = SUPER, SUPER_L, exec, rofi -show drun
bindl = , XF86AudioMute, exec, pactl set-sink-mute @DEFAULT_SINK@ toggle

# Bind using keycode instead of key name
bind = SUPER, code:36, exec, kitty   # code:36 = Return

# Repeating bind (held down)
binde = , right, resizeactive, 10 0

# Release-triggered bind
bindr = SUPER, SUPER_L, exec, rofi -show drun

# Mouse scroll bind
bind = SUPER, mouse_up, workspace, e+1
bind = SUPER, mouse_down, workspace, e-1

# Switch binds (lid, tablet mode, etc.)
bindl = , switch:Lid Switch, exec, systemctl suspend
bindl = , switch:on:Lid Switch, exec, hyprctl keyword monitor "eDP-1, disable"
bindl = , switch:off:Lid Switch, exec, hyprctl keyword monitor "eDP-1, preferred, auto, 1"
```

### 5.4 `workspace`

```ini
# Named workspaces
workspace = 1, name:web
workspace = 2, name:code, monitor:DP-1
workspace = 3, name:media, monitor:HDMI-A-1, default:true
workspace = special:scratchpad, on-created-empty:foot

# Workspace rules
workspace = 1, monitor:DP-1, default:true, persistent:true
workspace = name:gaming, monitor:DP-2, rounding:false, decorate:false
```

### 5.5 `windowrule` / `windowrulev2`

```ini
# windowrule = RULE, REGEX
# REGEX matches against window class by default
windowrule = float, ^(pavucontrol)$
windowrule = float, ^(blueman-manager)$
windowrule = size 800 600, ^(pavucontrol)$
windowrule = move 100 100, ^(myapp)$
windowrule = workspace 2, ^(firefox)$
windowrule = opacity 0.9, ^(kitty)$
windowrule = noblur, ^(firefox)$
windowrule = fullscreen, ^(gamescope)$
windowrule = tile, ^(Spotify)$
windowrule = pin, ^(stickynotes)$
windowrule = nofocus, ^()$    # empty class — unmanaged xwayland

# windowrulev2 = RULE, FILTERS
# More powerful: filter by class, title, xwayland, floating, fullscreen, etc.
windowrulev2 = float, class:^(xdg-desktop-portal-gtk)$
windowrulev2 = float, class:^(.*), title:^(Picture in picture)$
windowrulev2 = opacity 0.9 0.7, class:^(kitty)$    # active_opacity inactive_opacity
windowrulev2 = workspace 3, class:^(obs)$
windowrulev2 = monitor DP-2, class:^(discord)$
windowrulev2 = noblur, class:^(firefox)$, title:^(.*YouTube.*)$
windowrulev2 = suppressevent maximize, class:^(.*)$  # suppress maximize requests
windowrulev2 = nomaxsize, class:^(.*)$

# Available RULES:
# float              — make window floating
# tile               — make window tiled (undo float)
# fullscreen         — fullscreen the window (type 0)
# fullscreen 1       — maximize (type 1)
# fakefullscreen     — fake fullscreen (fills window, not compositor)
# pin                — pin to all workspaces (floating)
# move X Y           — set initial position (px or %)
# size W H           — set initial size (px or %)
# minsize W H        — minimum size
# maxsize W H        — maximum size
# workspace N        — open on workspace N
# workspace N silent — open on workspace N without switching
# monitor N/NAME     — open on specific monitor
# opacity ACTIVE [INACTIVE] — set opacity
# noblur             — disable blur for this window
# noanim             — disable animations
# nofocus            — never focus
# noshadow           — disable shadow
# noborder           — disable border
# bordersize N       — override border size
# rounding N         — override rounding
# decorate           — force decoration on/off
# center             — center the window on screen
# center 1           — center, considering reserved areas (gaps)
# stayfocused        — window never loses focus
# group              — add to group
# group set          — add to group and activate
# group new          — start new group
# group lock         — lock active in group
# group barred       — exclude from group
# tile               — force tile even if app requests float
# xray 1/0           — force blur xray
# idleinhibit CONDITION — inhibit idle: none, always, focus, fullscreen
# scrollmouse N      — override scroll sensitivity
# keepaspectratio    — maintain aspect ratio on resize
# bordercolor COLOR [INACTIVE_COLOR] — custom border color
# dimaround          — dim windows below
# renderunfocused    — render even when unfocused (useful for MPV)
# animation STYLE    — custom animation for this window
# tag TAG_NAME       — apply a tag (for later rule matching)
# plugin:PLUGIN_RULE — plugin-specific rules

# Available FILTERS for windowrulev2:
# class:REGEX        — window class
# title:REGEX        — window title
# initialclass:REGEX
# initialtitle:REGEX
# xwayland:0/1       — is XWayland window
# floating:0/1
# fullscreen:0/1
# pinned:0/1
# focus:0/1          — is focused
# workspace:N
# workspace:name:NAME
# onworkspace:SELECTOR
# monitor:N/NAME
# tag:TAG_NAME
```

### 5.6 `layerrule`

```ini
# layerrule = RULE, NAMESPACE_REGEX
layerrule = blur, ^(waybar)$
layerrule = ignorezero, ^(waybar)$
layerrule = blur, swaync-control-center
layerrule = blur, rofi
layerrule = ignorealpha 0.5, rofi
layerrule = noanim, ^(selection)$
layerrule = xray 1, ^(waybar)$

# Rules: blur, ignorezero, ignorealpha VALUE, noanim, xray 0/1, animation STYLE
```

### 5.7 Per-device input config

```ini
# device section: override input settings for a specific device
# Use hyprctl devices to get device names
device {
    name = epic-mouse-v1
    sensitivity = -0.5
    accel_profile = flat
}

device {
    name = at-translated-set-2-keyboard
    kb_layout = de
    kb_options = caps:escape
}
```

### 5.8 `submap`

```ini
# Define submaps (modal keybind layers, like vim modes)
bind = SUPER, R, submap, resize        # enter "resize" submap
submap = resize
    binde = , right, resizeactive, 10 0
    binde = , left,  resizeactive, -10 0
    binde = , up,    resizeactive, 0 -10
    binde = , down,  resizeactive, 0 10
    bind = , escape, submap, reset     # return to default
    bind = , return, submap, reset
submap = reset                         # end submap block
```

### 5.9 `plugin`

```ini
plugin {
    hyprexpo {
        columns = 5
        gap_size = 5
        bg_col = rgb(111111)
        workspace_method = center current
        enable_gesture = true
        gesture_fingers = 3
        gesture_distance = 300
        gesture_positive = true
    }
    # other plugin-specific config here
}
```

---

## 6. Dispatchers (used in `bind`)

```ini
# Window management
exec, COMMAND               # run a command
exec-once, COMMAND          # run once (different from keyword exec-once)
killactive                  # close focused window
closewindow, ADDRESS        # close by address
movetoworkspace, N          # move window to workspace N
movetoworkspacesilent, N    # move without switching
togglefloating              # toggle float
togglefloating, active      # same
setfloating                 # force float
settiled                    # force tile
fullscreen                  # fullscreen (type 0)
fullscreen, 1               # maximize (type 1)
fullscreen, 2               # fake fullscreen
fakefullscreen              # same as fullscreen 2
togglefullscreen            # toggle
dpms, on/off/toggle         # power monitor
pin                         # pin window
movefocus, l/r/u/d          # move focus direction
movewindow, l/r/u/d         # move window in tiling
swapwindow, l/r/u/d         # swap with neighbour
swapnext                    # swap with next in cycle
swapactiveworkspaces, MON1 MON2  # swap workspaces between monitors
centerwindow                # center floating window
cyclenext                   # cycle focus forward
cyclenext, prev             # cycle focus backward
focuswindow, REGEX          # focus window by class/title
bringactivetotop            # bring active to top (z-order)
togglegroup                 # create/destroy group
changegroupactive, f/b      # cycle group tabs
focuscurrentorlast          # toggle between current and last focused
alterzorder, top/bottom     # change z-order
focusmonitor, NAME/ID       # focus a monitor
movecurrentworkspacetomonitor, MON  # move workspace to monitor
focusworkspaceoncurrentmonitor, N   # focus workspace on current monitor
workspace, N                # switch to workspace N
workspace, e+1              # relative workspace
workspace, e-1
workspace, m+1              # relative on monitor
workspace, previous         # go to previous workspace
workspace, previous_per_monitor
workspace, name:NAME
workspace, special          # toggle special workspace
togglespecialworkspace      # toggle default special
togglespecialworkspace, NAME
movetoworkspace, special:NAME
resizeactive, W H           # resize active window (px, +/-)
resizewindowpixel, RULE, WINDOW
moveactive, X Y             # move active floating window
movewindowpixel, RULE, WINDOW
resizeglobal, RULE          # resize all on workspace
pseudo                      # toggle pseudotiling (dwindle)
togglesplit                 # toggle split direction (dwindle)
orientationleft/right/top/bottom/center  # master layout orientation
addmaster                   # add master (master layout)
removemaster
layoutmsg, COMMAND          # send message to current layout
pass, WINDOW                # pass keybind to window (global hotkeys)
sendshortcut, MODS KEY, WINDOW
mouse_movetopos, X Y        # warp mouse
mouse_movetofocus           # warp mouse to focused window
forcerenderwindow           # force a window to re-render
setprop, WINDOW, PROP, VALUE  # set window property dynamically
global, NAME                # pass bind to global shortcut (for OBS, etc.)
event, NAME                 # emit a custom event
nop                         # no-op (placeholder)
exit                        # exit Hyprland
```

---

## 7. Workspace Identifiers

```
1, 2, 3 ... 9, 10          # numbered
name:NAME                   # named
special                     # default special workspace
special:NAME                # named special workspace
e+N / e-N                  # relative (e.g., e+1 = next)
m+N / m-N                  # relative on current monitor
r+N / r-N                  # relative, create if needed
previous                    # previously active
previous_per_monitor
w[tv1]                     # workspace selector (1 tiled visible window)
f[N]                        # workspace selector (N floating windows)
```

---

## 8. Colors

```ini
col.active_border = rgb(ffffff)               # opaque
col.active_border = rgba(ffffffee)            # with alpha
col.active_border = 0xffffffff                # hex ARGB
col.active_border = rgba(ff0000ff) rgba(0000ffff) 45deg   # gradient (angle)
col.active_border = rgba(ff0000ff) rgba(00ff00ff) rgba(0000ffff) 120deg  # multi-stop
```

---

## 9. `source` and File Splitting

```ini
# Include another .conf file
source = ~/.config/hypr/keybinds.conf
source = ~/.config/hypr/windowrules.conf
source = $HOME/.config/hypr/monitors.conf

# Variables expand in source paths
$confDir = ~/.config/hypr
source = $confDir/colors.conf
```

---

## 10. `hyprctl` Runtime Control

```bash
hyprctl reload                          # reload config
hyprctl keyword general:gaps_in 10     # set a value live (not saved)
hyprctl dispatch exec kitty            # run a dispatcher
hyprctl activewindow                   # info about active window
hyprctl clients                        # list all windows
hyprctl monitors                       # list monitors
hyprctl workspaces                     # list workspaces
hyprctl devices                        # list input devices
hyprctl binds                          # list keybinds
hyprctl layers                         # list layers
hyprctl cursorpos                      # cursor position
hyprctl version                        # version info
hyprctl setprop address:0x... PROP VAL # set window property
hyprctl --batch "dispatch exec kitty ; keyword general:gaps_in 5"
```

---

## 11. Complete Minimal Example Config

```ini
# ~/.config/hypr/hyprland.conf

# Monitor
monitor = ,preferred,auto,1

# Autostart
exec-once = waybar
exec-once = dunst
exec-once = swww-daemon

# Environment
env = XCURSOR_SIZE,24

# Variables
$terminal = kitty
$menu = rofi -show drun
$mainMod = SUPER

# General
general {
    gaps_in = 5
    gaps_out = 10
    border_size = 2
    col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg
    col.inactive_border = rgba(595959aa)
    layout = dwindle
}

# Decoration
decoration {
    rounding = 10
    blur {
        enabled = true
        size = 3
        passes = 1
    }
    drop_shadow = true
    shadow_range = 4
}

# Animations
animations {
    enabled = true
    bezier = myBezier, 0.05, 0.9, 0.1, 1.05
    animation = windows, 1, 7, myBezier
    animation = fade, 1, 7, default
    animation = workspaces, 1, 6, default
}

# Input
input {
    kb_layout = us
    follow_mouse = 1
    touchpad {
        natural_scroll = false
    }
    sensitivity = 0
}

# Layout
dwindle {
    pseudotile = true
    preserve_split = true
}

# Keybinds
bind = $mainMod, Return, exec, $terminal
bind = $mainMod, Q, killactive
bind = $mainMod, M, exit
bind = $mainMod, E, exec, thunar
bind = $mainMod, V, togglefloating
bind = $mainMod, D, exec, $menu
bind = $mainMod, P, pseudo
bind = $mainMod, J, togglesplit
bind = $mainMod, F, fullscreen

# Move focus
bind = $mainMod, left, movefocus, l
bind = $mainMod, right, movefocus, r
bind = $mainMod, up, movefocus, u
bind = $mainMod, down, movefocus, d

# Switch workspaces
bind = $mainMod, 1, workspace, 1
bind = $mainMod, 2, workspace, 2
bind = $mainMod, 3, workspace, 3
bind = $mainMod, 4, workspace, 4
bind = $mainMod, 5, workspace, 5

# Move window to workspace
bind = $mainMod SHIFT, 1, movetoworkspace, 1
bind = $mainMod SHIFT, 2, movetoworkspace, 2
bind = $mainMod SHIFT, 3, movetoworkspace, 3

# Mouse window management
bindm = $mainMod, mouse:272, movewindow
bindm = $mainMod, mouse:273, resizewindow

# Scroll through workspaces
bind = $mainMod, mouse_down, workspace, e+1
bind = $mainMod, mouse_up, workspace, e-1

# Window rules
windowrulev2 = suppressevent maximize, class:^(.*)$
windowrulev2 = float, class:^(pavucontrol)$
windowrulev2 = float, class:^(nm-connection-editor)$
```

---

## 12. Hyprlang `#hyprlang` Pragma Reference

```ini
# hyprlang noerror true       — suppress errors for following lines
# hyprlang noerror false      — stop suppressing
# hyprlang if $VAR_NAME       — conditional block (var must be non-empty)
# hyprlang endif              — end conditional block
```