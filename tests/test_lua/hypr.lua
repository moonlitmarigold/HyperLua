-- This Hyprland lua config is auto translated from the old Hyprlang

-- Hyprland variables

hl.config({
    ecosystem = {
        enforce_permissions = 1,
    },
    general = {
        col = {
            active_border = { colors = {"rgba(33ccffee)", "rgba(00ff99ee)"}, angle = "45deg" },
            inactive_border = "rgba(595959aa)",
        },
        gaps_in = 5,
        gaps_out = 20,

        border_size = 2,

        -- # https://wiki.hypr.land/Configuring/Variables/#variable-types for info about colors

        -- # Set to true enable resizing windows by clicking and dragging on borders and gaps
        resize_on_border = false,

        -- # Please see https://wiki.hypr.land/Configuring/Tearing/ before you turn this on
        allow_tearing = false,

        layout = "dwindle",
    },
    decoration = {
        rounding = 10,
        rounding_power = 2,

        -- # Change transparency of focused and unfocused windows
        active_opacity = 1.0,
        inactive_opacity = 1.0,

        shadow = {
            enabled = true,
            range = 4,
            render_power = 3,
            color = "rgba(1a1a1aee)",
        },

        -- # https://wiki.hypr.land/Configuring/Variables/#blur
        blur = {
            enabled = true,
            size = 3,
            passes = 1,

            vibrancy = 0.1696,
        },
    },
    dwindle = {
        preserve_split = true, -- You probably want this
    },
    master = {
        new_status = "master",
    },
    misc = {
        force_default_wallpaper = -1, -- Set to 0 or 1 to disable the anime mascot wallpapers
        disable_hyprland_logo = false, -- If true disables the random hyprland logo / anime girl background. :(
    },
    input = {
        kb_layout = "us",
        kb_variant = "",
        kb_model = "",
        kb_options = "",
        kb_rules = "",

        follow_mouse = 1,

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.

        touchpad = {
            natural_scroll = false,
        },
    },
    device = {
        name = "epic-mouse-v1",
        sensitivity = -0.5,
    },
    windofdsfsdfsdfsdfsd = {
        -- # Fix some dragging issues with XWayland
        -- name = fix-xwayland-drags
        -- match:class = ^$
        -- match:title = ^$
        -- match:xwayland = true
        -- match:float = true
        -- match:fullscreen = false
        -- match:pin = false

        -- no_focus = true
    },
}, true)

-- Hyprland animations

hl.config({
    animations = {
        enabled = true,
    },
})


-- # Default curves, see https://wiki.hypr.land/Configuring/Animations/#curves
-- #        NAME,           X0,   Y0,   X1,   Y1
hl.curve("easeOutQuint", { type = "bezier", points = { {0.23, 1}, {0.32, 1} } })
hl.curve("easeInOutCubic", { type = "bezier", points = { {0.65, 0.05}, {0.36, 1} } })
hl.curve("linear", { type = "bezier", points = { {0, 0}, {1, 1} } })
hl.curve("almostLinear", { type = "bezier", points = { {0.5, 0.5}, {0.75, 1} } })
hl.curve("quick", { type = "bezier", points = { {0.15, 0}, {0.1, 1} } })

-- # Default animations, see https://wiki.hypr.land/Configuring/Animations/
-- #           NAME,          ONOFF, SPEED, CURVE,        [STYLE]
hl.animation({ leaf = "global", enabled = true, speed = 10, bezier = "default" })
hl.animation({ leaf = "border", enabled = true, speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "windows", enabled = true, speed = 4.79, bezier = "easeOutQuint" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 4.1, bezier = "easeOutQuint", style = "popin 87%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 1.49, bezier = "linear", style = "popin 87%" })
hl.animation({ leaf = "fadeIn", enabled = true, speed = 1.73, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut", enabled = true, speed = 1.46, bezier = "almostLinear" })
hl.animation({ leaf = "fade", enabled = true, speed = 3.03, bezier = "quick" })
hl.animation({ leaf = "layers", enabled = true, speed = 3.81, bezier = "easeOutQuint" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 4, bezier = "easeOutQuint", style = "fade" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 1.5, bezier = "linear", style = "fade" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 1.79, bezier = "almostLinear" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 1.39, bezier = "almostLinear" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "workspacesIn", enabled = true, speed = 1.21, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "workspacesOut", enabled = true, speed = 1.94, bezier = "almostLinear", style = "fade" })
hl.animation({ leaf = "zoomFactor", enabled = true, speed = 7, bezier = "quick" })

-- Hyprland start execs

hl.on("hyprland.start", function()
    hl.exec_cmd("$terminal")
    hl.exec_cmd("nm-applet &")
    hl.exec_cmd("waybar & hyprpaper & firefox")
    hl.exec_cmd("waybar")
end)

-- # This is an example Hyprland config file.
-- # Refer to the wiki for more information.
-- # https://wiki.hypr.land/Configuring/

-- # Please note not all available settings / options are set here.
-- # For a full list, see the wiki

-- # You can split this configuration into multiple files
-- # Create your files separately and then link them to this file like this:
-- # source = ~/.config/hypr/myColors.conf


-- ################
-- ### MONITORS ###
-- ################

-- # See https://wiki.hypr.land/Configuring/Monitors/
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto", })


-- ###################
-- ### MY PROGRAMS ###
-- ###################

-- # See https://wiki.hypr.land/Configuring/Keywords/

-- # Set programs that you use
local terminal = "kitty"
local fileManager = "dolphin"
local menu = "hyprlauncher"


-- #################
-- ### AUTOSTART ###
-- #################

-- # Autostart necessary processes (like notifications daemons, status bars, etc.)
-- # Or execute your favorite apps at launch like this:


hl.exec_cmd("$terminal")


-- #############################
-- ### ENVIRONMENT VARIABLES ###
-- #############################

-- # See https://wiki.hypr.land/Configuring/Environment-variables/

hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "24")


-- ###################
-- ### PERMISSIONS ###
-- ###################

-- # See https://wiki.hypr.land/Configuring/Permissions/
-- # Please note permission changes here require a Hyprland restart and are not applied on-the-fly
-- # for security reasons


hl.permission("/usr/(bin|local/bin)/grim", "screencopy", "allow")
hl.permission("/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland", "screencopy", "allow")
hl.permission("/usr/(bin|local/bin)/hyprpm", "plugin", "allow")


-- #####################
-- ### LOOK AND FEEL ###
-- #####################

-- # Refer to https://wiki.hypr.land/Configuring/Variables/

-- # https://wiki.hypr.land/Configuring/Variables/#general

-- # https://wiki.hypr.land/Configuring/Variables/#decoration

-- # https://wiki.hypr.land/Configuring/Variables/#animations

-- # Ref https://wiki.hypr.land/Configuring/Workspace-Rules/
-- # "Smart gaps" / "No gaps when only"
-- # uncomment all if you wish to use that.
hl.workspace_rule({ workspace = "w[tv1]", gapsout = 0, gapsin = 0, })
hl.workspace_rule({ workspace = "f[1]", gapsout = 0, gapsin = 0, })
-- # windowrule {
-- #     name = no-gaps-wtv1
-- #     match:float = false
-- #     match:workspace = w[tv1]
-- #
-- #     border_size = 0
-- #     rounding = 0
-- # }
-- #
-- # windowrule {
-- #     name = no-gaps-f1
-- #     match:float = false
-- #     match:workspace = f[1]
-- #
-- #     border_size = 0
-- #     rounding = 0
-- # }

-- # See https://wiki.hypr.land/Configuring/Dwindle-Layout/ for more

-- # See https://wiki.hypr.land/Configuring/Master-Layout/ for more

-- # https://wiki.hypr.land/Configuring/Variables/#misc


-- #############
-- ### INPUT ###
-- #############

-- # https://wiki.hypr.land/Configuring/Variables/#input

-- # See https://wiki.hypr.land/Configuring/Gestures
-- gesture = 3, horizontal, workspace

-- # Example per-device config
-- # See https://wiki.hypr.land/Configuring/Keywords/#per-device-input-configs for more


-- ###################
-- ### KEYBINDINGS ###
-- ###################

-- # See https://wiki.hypr.land/Configuring/Keywords/
local mainMod = "SUPER" -- Sets "Windows" key as main modifier

-- # Example binds, see https://wiki.hypr.land/Configuring/Binds/ for more
-- bind = $mainMod, Q, exec, $terminal
-- bind = $mainMod, C, killactive,
-- bind = $mainMod, M, exec, command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch exit
-- bind = $mainMod, E, exec, $fileManager
-- bind = $mainMod, V, togglefloating,
-- bind = $mainMod, R, exec, $menu
-- bind = $mainMod, P, pseudo, -- dwindle
-- bind = $mainMod, J, layoutmsg, togglesplit -- dwindle

-- # Move focus with mainMod + arrow keys
-- bind = $mainMod, left, movefocus, l
-- bind = $mainMod, right, movefocus, r
-- bind = $mainMod, up, movefocus, u
-- bind = $mainMod, down, movefocus, d

-- # Switch workspaces with mainMod + [0-9]
-- bind = $mainMod, 1, workspace, 1
-- bind = $mainMod, 2, workspace, 2
-- bind = $mainMod, 3, workspace, 3
-- bind = $mainMod, 4, workspace, 4
-- bind = $mainMod, 5, workspace, 5
-- bind = $mainMod, 6, workspace, 6
-- bind = $mainMod, 7, workspace, 7
-- bind = $mainMod, 8, workspace, 8
-- bind = $mainMod, 9, workspace, 9
-- bind = $mainMod, 0, workspace, 10

-- # Move active window to a workspace with mainMod + SHIFT + [0-9]
-- bind = $mainMod SHIFT, 1, movetoworkspace, 1
-- bind = $mainMod SHIFT, 2, movetoworkspace, 2
-- bind = $mainMod SHIFT, 3, movetoworkspace, 3
-- bind = $mainMod SHIFT, 4, movetoworkspace, 4
-- bind = $mainMod SHIFT, 5, movetoworkspace, 5
-- bind = $mainMod SHIFT, 6, movetoworkspace, 6
-- bind = $mainMod SHIFT, 7, movetoworkspace, 7
-- bind = $mainMod SHIFT, 8, movetoworkspace, 8
-- bind = $mainMod SHIFT, 9, movetoworkspace, 9
-- bind = $mainMod SHIFT, 0, movetoworkspace, 10

-- # Example special workspace (scratchpad)
-- bind = $mainMod, S, togglespecialworkspace, magic
-- bind = $mainMod SHIFT, S, movetoworkspace, special:magic

-- # Scroll through existing workspaces with mainMod + scroll
-- bind = $mainMod, mouse_down, workspace, e+1
-- bind = $mainMod, mouse_up, workspace, e-1

-- # Move/resize windows with mainMod + LMB/RMB and dragging
-- bindm = $mainMod, mouse:272, movewindow
-- bindm = $mainMod, mouse:273, resizewindow

-- # Laptop multimedia keys for volume and LCD brightness
-- bindel = ,XF86AudioRaiseVolume, exec, wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+
-- bindel = ,XF86AudioLowerVolume, exec, wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-
-- bindel = ,XF86AudioMute, exec, wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle
-- bindel = ,XF86AudioMicMute, exec, wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle
-- bindel = ,XF86MonBrightnessUp, exec, brightnessctl -e4 -n2 set 5%+
-- bindel = ,XF86MonBrightnessDown, exec, brightnessctl -e4 -n2 set 5%-

-- # Requires playerctl
-- bindl = , XF86AudioNext, exec, playerctl next
-- bindl = , XF86AudioPause, exec, playerctl play-pause
-- bindl = , XF86AudioPlay, exec, playerctl play-pause
-- bindl = , XF86AudioPrev, exec, playerctl previous -- Test Inline Comment

-- ##############################
-- ### WINDOWS AND WORKSPACES ###
-- ##############################

-- # See https://wiki.hypr.land/Configuring/Window-Rules/ for more
-- # See https://wiki.hypr.land/Configuring/Workspace-Rules/ for workspace rules

-- # Example windowrules that are useful

windowrule = {
    -- # Ignore maximize requests from all apps. You'll probably like this.
    name = "suppress-maximize-events",
    match = { class = ".*" },

    suppress_event = "maximize",
},


-- # Hyprland-run windowrule
windowrule = {

    name = "move-hyprland-run", -- test
    match = { class = "hyprland-run" },

    move = "20 monitor_h-120",
    float = true,
},

hl.window_rule({ name = "windowrule1", match = { class = "^(pavucontrol)$" }, float = true, })
hl.window_rule({ name = "windowrule2", match = { class = "^(blueman-manager)$" }, float = true, })
hl.window_rule({ name = "windowrule3", match = { class = "^(pavucontrol)$" }, size = "800 600", })
hl.window_rule({ name = "windowrule4", match = { class = "^(myapp)$" }, move = "100 100", })
hl.window_rule({ name = "windowrule5", match = { class = "^(firefox)$" }, workspace = 2, })
hl.window_rule({ name = "windowrule6", match = { class = "^(kitty)$" }, opacity = { active = 0.9, }, })
hl.window_rule({ name = "windowrule7", match = { class = "^(firefox)$" }, no_blur = true, })
hl.window_rule({ name = "windowrule8", match = { class = "^(gamescope)$" }, fullscreen = true, })
hl.window_rule({ name = "windowrule9", match = { class = "^(Spotify)$" }, float = true, })
hl.window_rule({ name = "windowrule10", match = { class = "^(stickynotes)$" }, pin = true, })
hl.window_rule({ name = "windowrule11", match = { class = "^()$" }, no_focus = true, }) -- empty class — unmanaged xwayland

hl.window_rule({ name = "windowrule12", match = { class = "^(xdg-desktop-portal-gtk)$", }, float = true, })
hl.window_rule({ name = "windowrule13", match = { class = "^(.*)", title = "^(Picture in picture)$", }, float = true, })
hl.window_rule({ name = "windowrule14", match = { class = "^(kitty)$", }, opacity = { active = 0.9, inactive = 0.7, }, })
hl.window_rule({ name = "windowrule15", match = { class = "^(obs)$", }, workspace = 3, })
hl.window_rule({ name = "windowrule16", match = { class = "^(discord)$", }, monitor = "DP-2", })
hl.window_rule({ name = "windowrule17", match = { class = "^(firefox)$", title = "^(.*YouTube.*)$", }, no_blur = true, })
hl.window_rule({ name = "windowrule18", match = { class = "^(.*)$", }, suppress_event = "maximize", })
hl.window_rule({ name = "windowrule19", match = { class = "^(.*)$", }, no_max_size = true, })
hl.window_rule({ name = "windowrule20", match = { class = "^(myapp)$", }, move = "100 100", })
hl.window_rule({ name = "windowrule21", match = { class = "^(pavucontrol)$", }, size = "800 600", })
hl.window_rule({ name = "windowrule22", match = { class = "^(important)$", }, border_color = { active = "rgb(ff0000)", inactive = "rgb(00ff00)", }, })
hl.window_rule({ name = "windowrule23", match = { class = "^(dialog)$", }, center = true, })

require("test_sub_folder/test.conf")

hl.exec_cmd("~/.config/hypr/reload_script.sh")