-- HyprLua Configuration
hl.monitor("DP-0-0", mode="preferred")

local terms = {"kitty", "alacritty"}
local menu = "~/.local/bin/hyprlauncher"
local browser = "firefox"

hl.env("XCURSOR_SIZE", "24")

hl.config({
    general = {
        gaps_in  = 5,
        gaps_out = 20,
        border_size = 2,
        col = {
            active_border   = {"rgba(33ccffee)", "rgba(00ff99ee)"},
            inactive_border = "rgba(595959aa)",
        },
    },
}, true)

hl.bind(super.."+q", hl.dsp.window.close())
hl.bind(super.."+c", hl.dsp.window.close())
hl.bind(super.."+e", hl.dsp.exec_cmd("dolphin"))
hl.bind(super.."+r", hl.dsp.exec_cmd(menu))
hl.bind(super.."+v", hl.dsp.window.float())
hl.bind(super.."+p", hl.dsp.window.pseudo())

hl.window_rule({
    name  = "fix-xwayland-drags",
    match = {
        class = "^$",
        window_role = ".*",
    },
    no_focus = true,
})

hl.window_rule({
    name = "move-hyprland-run",
    match = { class = "hyprland-run" },
    move = "20 monitor_dp-1",
    float = true,
})

-- Workspace rules
hl.workspace_rule({
    workspace = "w[1]",
    gaps_out = 0,
})

-- Layer rules
hl.layer_rule({
    name = "overlay-layer",
    match = { namespace = "overlay" },
    no_anim = true,
})

-- Animation config
hl.animation({
    leaf = "windows",
    enabled = true,
    speed = 4.79,
    spring = "easy",
})
