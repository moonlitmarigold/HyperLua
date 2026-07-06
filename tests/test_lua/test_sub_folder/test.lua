-- This Hyprland lua config is auto translated from the old Hyprlang

hl.window_rule({ name = "windowrule24", match = { class = "my-window", }, border_size 10 })

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