# Hyprland Lua Configuration Reference (0.55+) — with hyprlang Translations

> Companion to `hyprland_hyprlang_reference.md`. Since **Hyprland 0.55**, the config file is
> `~/.config/hypr/hyprland.lua` (instead of `hyprland.conf`). The old `hyprlang` `.conf` syntax
> is deprecated but still works if no `.lua` file exists. This doc covers the Lua API and maps
> every old construct to its new equivalent.

---

## 0. Core Concepts

- Config file: `$XDG_CONFIG_HOME/hypr/hyprland.lua` (usually `~/.config/hypr/hyprland.lua`)
- All Hyprland-specific functionality lives under the global table **`hl`**
- Dispatchers live under **`hl.dsp`**
- Plain Lua is used for variables, loops, conditionals, functions — no more custom `$var`/arithmetic-in-braces syntax
- Split configs with Lua's native `require()` instead of `source =`
- Reload still happens automatically on save, or manually via `hyprctl reload`
- Lua standard library is available; scripts can run arbitrary code, so only use configs you trust
- Long-running scripts get killed by a watchdog timeout (anti-freeze protection)

```lua
-- Comment syntax is now Lua's --, not #
require("mycolors")          -- relative to hyprland.lua, "/" or "." separators both work
require("keybinds/main")
```

---

## 1. Syntax Translation Cheat Sheet

| Old (hyprlang `.conf`) | New (Lua) |
|---|---|
| `# comment` | `-- comment` |
| `$var = value` | `local var = value` |
| `option = $var` | `option = var` |
| `{{$a + $b}}` | `a + b` (plain Lua arithmetic) |
| `source = path.conf` | `require("path")` |
| `category { option = val }` | `hl.config({ category = { option = val } })` |
| `monitor = ...` | `hl.monitor({ ... })` |
| `bind = ...` | `hl.bind(...)` |
| `windowrule` / `windowrulev2` | `hl.window_rule({ ... })` |
| `layerrule` | `hl.layer_rule({ ... })` |
| `workspace = ...` (rule) | `hl.workspace_rule({ ... })` |
| `bezier = ...` | `hl.curve(name, { type = "bezier", points = {...} })` |
| `animation = ...` | `hl.animation({ leaf = ..., ... })` |
| `exec-once = cmd` | `hl.on("hyprland.start", function() hl.exec_cmd("cmd") end)` |
| `exec = cmd` | runs every reload — use `hl.exec_cmd("cmd")` directly in the file body |
| `env = VAR,value` | `hl.env("VAR", "value")` |
| `device { name = ... }` | `hl.device({ name = ..., ... })` |
| `submap = name ... binds ... submap = reset` | `hl.define_submap(name, ...)` / `hl.dsp.submap(name)` (see §8) |
| `plugin { name { opt = val } }` | usually still `hl.config({ plugin = { name = {...} } })` |
| `# hyprlang noerror true` | not needed — per-`require()` files have isolated error scopes |
| `# hyprlang if $VAR` / `endif` | plain Lua `if os.getenv("VAR") ~= "" then ... end` |
| `hyprctl keyword cat:opt val` | `hl.config({ cat = { opt = val } })` |

---

## 2. Options — `hl.config({...})`

Every old `category { }` block becomes a nested Lua table passed to `hl.config()`. You can call
`hl.config()` multiple times; each call merges/updates just the keys you pass.

```lua
hl.config({
    category = { value = ... },
    category2 = { value2 = ... },
})
```

### 2.1 `general` (old `general {}`)

```lua
hl.config({
    general = {
        gaps_in = 5,
        gaps_out = 20,
        border_size = 2,
        col = {
            active_border = { colors = {"rgba(33ccffee)", "rgba(00ff99ee)"}, angle = 45 },
            inactive_border = "rgba(595959aa)",
        },
        resize_on_border = false,
        allow_tearing = false,
        layout = "dwindle",
    },
})
```

**Translation note:** `col.active_border` used to be a single string with an optional inline
gradient/angle (`rgba(...) rgba(...) 45deg`). It's now a **table**: `{ colors = {...}, angle = N }`.

| Old | New |
|---|---|
| `col.active_border = rgba(33ccffee) rgba(00ff99ee) 45deg` | `col = { active_border = { colors = {"rgba(33ccffee)", "rgba(00ff99ee)"}, angle = 45 } }` |
| `col.inactive_border = rgba(595959aa)` | `col = { inactive_border = "rgba(595959aa)" }` (plain string still fine, no gradient) |

### 2.2 `decoration` (old `decoration {}` + `blur {}`)

```lua
hl.config({
    decoration = {
        rounding = 10,
        rounding_power = 2,          -- NEW: controls rounding curve shape
        active_opacity = 1.0,
        inactive_opacity = 1.0,
        shadow = {                    -- was top-level drop_shadow/shadow_range/col.shadow
            enabled = true,
            range = 4,
            render_power = 3,
            color = 0xee1a1a1a,        -- now a single ARGB int, not col.shadow rgba string
        },
        blur = {
            enabled = true,
            size = 3,
            passes = 1,
            vibrancy = 0.1696,
        },
    },
})
```

| Old | New |
|---|---|
| `drop_shadow = true` | `shadow = { enabled = true }` |
| `shadow_range = 4` | `shadow = { range = 4 }` |
| `shadow_render_power = 3` | `shadow = { render_power = 3 }` |
| `col.shadow = rgba(1a1a1aee)` | `shadow = { color = 0xee1a1a1a }` |
| `blur { enabled = true ... }` | `decoration.blur = { enabled = true, ... }` (nested table, same fields) |

### 2.3 `animations` — now split into `hl.curve()` + `hl.animation()`

Old:
```ini
bezier = myBezier, 0.05, 0.9, 0.1, 1.05
animation = windows, 1, 7, myBezier
animation = windowsOut, 1, 7, default, popin 80%
```

New:
```lua
hl.curve("myBezier", { type = "bezier", points = { {0.05, 0.9}, {0.1, 1.05} } })

hl.animation({ leaf = "windows", enabled = true, speed = 7, bezier = "myBezier" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 7, bezier = "default", style = "popin 80%" })

-- Enable/disable animations globally still goes through hl.config:
hl.config({ animations = { enabled = true } })
```

**Spring curves (new in the Lua era).** `hl.curve()` isn't limited to beziers anymore — you can
also define a physics **spring** curve, and reference it from an animation with `spring = NAME`
(instead of `bezier = NAME`). There was no old hyprlang equivalent for spring-based animations.

```lua
hl.curve("easy", { type = "spring", mass = 1, stiffness = 71.2633, dampening = 15.8273644 })

hl.animation({ leaf = "windows",   enabled = true, speed = 4.79, spring = "easy" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 4.1,  spring = "easy", style = "popin 87%" })
```
> Note the field is spelled **`dampening`** (not `damping`), and it's a curve, not an animation
> field — an `hl.animation({...})` picks a curve by either `bezier = "..."` **or** `spring = "..."`,
> never both.

| Old field | New field |
|---|---|
| `bezier = NAME, X0,Y0,X1,Y1` | `hl.curve(NAME, { type = "bezier", points = { {X0,Y0}, {X1,Y1} } })` |
| *(no old equivalent)* | `hl.curve(NAME, { type = "spring", mass = M, stiffness = S, dampening = D })` |
| `animation = EVENT, ONOFF, SPEED, CURVE, STYLE` | `hl.animation({ leaf = EVENT, enabled = (ONOFF==1), speed = SPEED, bezier = CURVE, style = STYLE })` |
| `animation = EVENT, ONOFF, SPEED, SPRINGNAME` | `hl.animation({ leaf = EVENT, enabled = (ONOFF==1), speed = SPEED, spring = SPRINGNAME })` |
| Event names (`windows`, `border`, `fade`, `workspaces`, ...) | Same names, passed as `leaf = "..."` |

Animation leaf names available in the example config: `global`, `border`, `windows`, `windowsIn`,
`windowsOut`, `fadeIn`, `fadeOut`, `fade`, `layers`, `layersIn`, `layersOut`, `fadeLayersIn`,
`fadeLayersOut`, `workspaces`, `workspacesIn`, `workspacesOut`, `zoomFactor` (new, for cursor zoom).

### 2.4 `input` (old `input {}` + `touchpad {}`)

```lua
hl.config({
    input = {
        kb_layout = "us",
        kb_variant = "",
        kb_model = "",
        kb_options = "",
        kb_rules = "",
        follow_mouse = 1,
        sensitivity = 0,
        touchpad = {
            natural_scroll = false,
        },
    },
})
```
Structurally identical to the old `input { touchpad { } }` nesting — just wrapped in `hl.config()`.

### 2.5 `gestures` — now `hl.gesture({...})` per-gesture, not a flat category

Old:
```ini
gestures {
    workspace_swipe = true
    workspace_swipe_fingers = 3
}
```

New:
```lua
hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = "workspace",
})
```

**Translation note:** gestures moved from a single flat options block to discrete gesture
registrations — you can now define multiple independent gestures (e.g. one for workspace swipe,
another for a custom action) instead of one fixed `workspace_swipe_*` set of options.

`hl.gesture()` fields (required: `fingers`, `direction`, `action`; the rest optional):

| Field | Type | Meaning |
|---|---|---|
| `fingers` | integer | number of fingers (e.g. `3`) |
| `direction` | string | `"horizontal"`, `"vertical"`, etc. |
| `action` | string \| function | built-in action name (e.g. `"workspace"`) **or** a Lua callback |
| `mods` | string | modifier keys required during the gesture |
| `scale` | number | sensitivity/scale factor |
| `mode` | string | gesture mode |
| `zoom_level` | number | for zoom-style gestures |
| `workspace_name` | string | target workspace for workspace gestures |
| `disable_inhibit` | boolean | ignore inhibitors |

Because `action` accepts a function, a gesture can now run arbitrary Lua — not possible with the
old fixed `workspace_swipe_*` options.

### 2.6 `group`, `misc`, `binds`, `xwayland`, `render`, `cursor`, `debug`, `dwindle`, `master`

All of these keep their **option names** but are wrapped in `hl.config({ category = {...} })`
the same way as `general`:

```lua
hl.config({
    dwindle = { preserve_split = true },
})
hl.config({
    master = { new_status = "master" },
})
hl.config({
    misc = {
        force_default_wallpaper = -1,
        disable_hyprland_logo = false,
    },
})
```

| Old | New |
|---|---|
| `dwindle { preserve_split = true }` | `hl.config({ dwindle = { preserve_split = true } })` |
| `master { new_status = master }` | `hl.config({ master = { new_status = "master" } })` |
| `misc { force_default_wallpaper = -1 }` | `hl.config({ misc = { force_default_wallpaper = -1 } })` |

A **new layout category** appears in Lua configs: `scrolling` (the Scrolling layout), e.g.:
```lua
hl.config({ scrolling = { fullscreen_on_one_column = true } })
```

---

## 3. Monitors

Old:
```ini
monitor = DP-1, 1920x1080@144, 0x0, 1
monitor = ,preferred,auto,1
```

New:
```lua
hl.monitor({
    output = "DP-1",
    mode = "1920x1080@144",
    position = "0x0",
    scale = 1,
})

-- catch-all
hl.monitor({
    output = "",
    mode = "preferred",
    position = "auto",
    scale = "auto",
})
```

| Old positional field | New named field |
|---|---|
| 1st: monitor name | `output` |
| 2nd: resolution@refresh | `mode` |
| 3rd: position | `position` |
| 4th: scale | `scale` |
| `transform, N` | `transform = N` |
| `bitdepth, N` | `bitdepth = N` |
| `mirror, NAME` | `mirror = "NAME"` |
| `disable` | `mode = "disable"` (fields per the Lua bindings: `mode`, `position`, `scale`, `transform`, `vrr`, `mirror`, `bitdepth`, `icc`) |

---

## 4. Binds

This is the area with the biggest structural change: dispatchers are no longer bare strings —
they're **function calls** under `hl.dsp`, and binds can take **Lua functions** as handlers.

### 4.1 Basic translation

Old:
```ini
bind = SUPER, Q, exec, kitty
bind = SUPER, C, killactive
bind = SUPER SHIFT, F, fullscreen, 1
```

New:
```lua
local mainMod = "SUPER"
hl.bind(mainMod .. " + Q", hl.dsp.exec_cmd("kitty"))
hl.bind(mainMod .. " + C", hl.dsp.window.close())
hl.bind(mainMod .. " + SHIFT + F", hl.dsp.window.fullscreen({ mode = "maximize" }))
```

| Old | New |
|---|---|
| `bind = MODS, KEY, DISPATCHER, ARGS` | `hl.bind("MODS + KEY", hl.dsp.dispatcher({ args... }))` |
| Key string format `SUPER, Q` (comma) | Single string `"SUPER + Q"` (plus signs) |
| `exec, CMD` | `hl.dsp.exec_cmd("CMD")` |
| `killactive` | `hl.dsp.window.close()` |
| `togglefloating` | `hl.dsp.window.float({ action = "toggle" })` |
| `fullscreen` / `fullscreen, 1` | `hl.dsp.window.fullscreen({ mode = "fullscreen" / "maximize" })` |
| `pseudo` | `hl.dsp.window.pseudo()` |
| `togglesplit` | `hl.dsp.layout("togglesplit")` |
| `movefocus, l/r/u/d` | `hl.dsp.focus({ direction = "left"/"right"/"up"/"down" })` |
| `workspace, N` | `hl.dsp.focus({ workspace = N })` |
| `movetoworkspace, N` | `hl.dsp.window.move({ workspace = N })` |
| `workspace, e+1` / `e-1` | `hl.dsp.focus({ workspace = "e+1" })` (string still works for relative selectors) |
| `togglespecialworkspace, NAME` | `hl.dsp.workspace.toggle_special("NAME")` |
| mouse binds (`bindm`) | `hl.bind("MODS + mouse:272", hl.dsp.window.drag(), { mouse = true })` |
| scroll binds (`mouse_up`/`mouse_down`) | unchanged string token, still passed in the key string: `"SUPER + mouse_down"` |
| `bindl` (works when locked) | `{ locked = true }` option table, 3rd arg to `hl.bind` |
| `binde` (repeat while held) | `{ repeating = true }` option |
| `bindr` (on release) | `{ release = true }` option |
| `bindn` (non-consuming) | `{ non_consuming = true }` |
| `bindt` (transparent) | `{ transparent = true }` |
| `bindi` (ignore mods) | `{ ignore_mods = true }` |
| `bindm` (mouse) | `{ mouse = true }` |
| combined flag letters (`bindel`, `bindle`, ...) | combine keys in the one options table: `{ repeating = true, locked = true }` |
| keycodes (`code:36`) | same: `hl.bind("SUPER + code:36", ...)` |

The full `hl.bind(keys, dispatcher, opts?)` options table (all boolean unless noted) is:
`repeating`, `locked`, `release`, `non_consuming`, `transparent`, `ignore_mods`, `mouse`,
`dont_inhibit`, `long_press`, `submap_universal`, `click`, `drag`, `description`/`desc` (string),
and `device = { inclusive?, list? }` to scope a bind to specific input devices. `hl.bind()`
returns a **keybind handle** (see §4.4).

### 4.2 Loops replace repetitive binds

Old (10 separate lines per workspace number):
```ini
bind = SUPER, 1, workspace, 1
bind = SUPER, 2, workspace, 2
...
```

New (one loop):
```lua
for i = 1, 10 do
    local key = i % 10  -- 10 maps to key 0
    hl.bind(mainMod .. " + " .. key, hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end
```

### 4.3 Multi-action binds: Lua functions instead of submaps/chained dispatchers

Old workaround (separate dispatcher per key, or hacks):
```ini
bind = SUPER, TAB, cyclenext
bind = SUPER, TAB, bringactivetotop
```

New (single bind, sequential logic in a function):
```lua
hl.bind("SUPER + Tab", function()
    hl.dispatch(hl.dsp.window.cycle_next())
    hl.dispatch(hl.dsp.window.bring_to_top())
end)
```

### 4.4 Bind handles — new capability, no old equivalent

```lua
local closeWindowBind = hl.bind(mainMod .. " + C", hl.dsp.window.close())
-- closeWindowBind:set_enabled(false)   -- can disable/re-enable a bind at runtime
```

There was **no way to toggle individual binds at runtime** in old hyprlang; this is new.

### 4.5 Switch binds

| Old | New |
|---|---|
| `bindl = , switch:NAME, exec, cmd` | `hl.bind("switch:NAME", hl.dsp.exec_cmd("cmd"), { locked = true })` |
| `bindl = , switch:on:NAME, exec, cmd` | `hl.bind("switch:on:NAME", hl.dsp.exec_cmd("cmd"), { locked = true })` |
| `bindl = , switch:off:NAME, exec, cmd` | `hl.bind("switch:off:NAME", hl.dsp.exec_cmd("cmd"), { locked = true })` |

---

## 5. Window Rules

Old (`windowrule` / `windowrulev2` — two separate, increasingly confusing keywords):
```ini
windowrule = float, ^(pavucontrol)$
windowrulev2 = float, class:^(xdg-desktop-portal-gtk)$
windowrulev2 = opacity 0.9 0.7, class:^(kitty)$
windowrulev2 = suppressevent maximize, class:^(.*)$
```

New (single `hl.window_rule({...})` call, `match` table for filters, top-level keys for effects):
```lua
hl.window_rule({
    name = "float-pavucontrol",      -- NEW: rules now have names (useful for set_enabled, debugging)
    match = { class = "^(pavucontrol)$" },
    float = true,
})

hl.window_rule({
    name = "kitty-opacity",
    match = { class = "^(kitty)$" },
    opacity = { active = 0.9, inactive = 0.7 },
})

hl.window_rule({
    name = "suppress-maximize-events",
    match = { class = ".*" },
    suppress_event = "maximize",
})

hl.window_rule({
    name = "fix-xwayland-drags",
    match = {
        class = "^$",
        title = "^$",
        xwayland = true,
        float = true,
        fullscreen = false,
        pin = false,
    },
    no_focus = true,
})
```

| Old | New |
|---|---|
| `windowrule = float, REGEX` (matches class by default) | `match = { class = "REGEX" }, float = true` |
| `windowrulev2 = RULE, class:REGEX` | `match = { class = "REGEX" }` |
| `windowrulev2 = RULE, title:REGEX` | `match = { title = "REGEX" }` |
| `windowrulev2 = RULE, xwayland:1` | `match = { xwayland = true }` |
| `windowrulev2 = RULE, floating:1` | `match = { float = true }` |
| `windowrulev2 = RULE, fullscreen:1` | `match = { fullscreen = true }` |
| `windowrulev2 = RULE, pinned:1` | `match = { pin = true }` |
| `windowrulev2 = RULE, workspace:N` | `match = { workspace = N }` |
| `float` | `float = true` |
| `tile` | `float = false` |
| `move X Y` | `move = "X Y"` |
| `size W H` | `size = "W H"` |
| `opacity A [I]` | `opacity = { active = A, inactive = I }` |
| `workspace N` | `workspace = N` |
| `noblur` | `no_blur = true` (verify exact key against current wiki) |
| `nofocus` | `no_focus = true` |
| `suppressevent maximize` | `suppress_event = "maximize"` |
| `pin` | `pin = true` |
| *(no name field existed)* | `name = "my-rule"` — every rule can now be named and later toggled |

**Translation note:** the old `windowrule` (class-string-only) vs `windowrulev2` (filter-table)
split is **gone** — there is now just one `hl.window_rule()` form, structurally like the old v2
but as native Lua tables instead of comma-separated strings.

### 5.1 Rule handles

```lua
local suppressMaximizeRule = hl.window_rule({ ... })
-- suppressMaximizeRule:set_enabled(false)
```
Same new capability as bind handles — rules can be runtime-toggled, which had no `.conf` equivalent.

---

## 6. Layer Rules

Old:
```ini
layerrule = blur, ^(waybar)$
layerrule = ignorealpha 0.5, rofi
```

New:
```lua
hl.layer_rule({
    name = "no-anim-overlay",
    match = { namespace = "^my-overlay$" },
    no_anim = true,
})
```

| Old | New |
|---|---|
| `layerrule = RULE, NAMESPACE_REGEX` | `match = { namespace = "NAMESPACE_REGEX" }, RULE = true/value` |
| `blur` | `blur = true` |
| `noanim` | `no_anim = true` |
| `ignorealpha VALUE` | `ignore_alpha = VALUE` (verify exact casing on current wiki) |

Layer rules return a handle too:
```lua
local overlayLayerRule = hl.layer_rule({ name = "no-anim-overlay", ... })
-- overlayLayerRule:set_enabled(false)
```

---

## 7. Workspace Rules

Old:
```ini
workspace = name:coding, monitor:DP-1, default:true, gaps_in:0
```

New:
```lua
hl.workspace_rule({
    workspace = "name:coding",
    monitor = "DP-1",
    default = true,
    gaps_in = 0,
})
```

Workspace identifiers (`name:X`, `e+1`, `special:X`, `w[tv1]`, `f[1]`, etc.) are **unchanged** —
only the wrapping syntax moved from `key:value` comma lists to a Lua table.

```lua
-- "Smart gaps" example from the official template
hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
hl.workspace_rule({ workspace = "f[1]", gaps_out = 0, gaps_in = 0 })

-- equivalent effect via window_rule (also shown in official template)
hl.window_rule({
    name = "no-gaps-wtv1",
    match = { float = false, workspace = "w[tv1]" },
    border_size = 0,
    rounding = 0,
})
```

---

## 8. Submaps

Submaps **are** exposed in the Lua API, in two complementary ways:

- **`hl.define_submap(name, reset_or_fn, fn?)`** — declares a submap and the binds that live
  inside it. You pass the submap name and a function that registers its binds; entering `"reset"`
  (or an empty submap) returns to the default keymap.
- **`hl.dsp.submap(name)`** — a dispatcher (bind *into* a submap, or escape a stuck one with
  `hyprctl dispatch 'hl.dsp.submap("reset")'`).
- **`hl.get_current_submap()`** — returns the name of the active submap (new; no `.conf` equivalent).

Old:
```ini
bind = SUPER, R, submap, resize
submap = resize
binde = , right, resizeactive, 10 0
bind  = , escape, submap, reset
submap = reset
```

New:
```lua
hl.bind("SUPER + R", hl.dsp.submap("resize"))

hl.define_submap("resize", function()
    hl.bind("right",  hl.dsp.window.resize({ x = 10, y = 0 }), { repeating = true })
    hl.bind("escape", hl.dsp.submap("reset"))
end)
```

| Old | New |
|---|---|
| `submap = NAME` … `submap = reset` block | `hl.define_submap("NAME", function() ... end)` |
| `bind = MODS, KEY, submap, NAME` | `hl.bind("MODS + KEY", hl.dsp.submap("NAME"))` |
| escape a stuck submap | `hyprctl dispatch 'hl.dsp.submap("reset")'` |
| *(no old equivalent)* | `hl.get_current_submap()` |

For multi-step modal binds you can alternatively manage state directly with a Lua closure instead
of a named submap. Exact dispatcher argument shapes are still evolving post-0.55 — cross-check the
**Binds** wiki page and the shipped `hl.meta.lua` stubs.

---

## 9. Devices (per-input-device config)

Old:
```ini
device {
    name = epic-mouse-v1
    sensitivity = -0.5
}
```

New:
```lua
hl.device({
    name = "epic-mouse-v1",
    sensitivity = -0.5,
})
```
Structurally identical — just a function call instead of a block.

---

## 10. Environment Variables

Old:
```ini
env = XCURSOR_SIZE,24
```

New:
```lua
hl.env("XCURSOR_SIZE", "24")
```

---

## 11. Autostart (`exec` / `exec-once`)

Old:
```ini
exec-once = waybar
exec = ~/.config/hypr/reload_script.sh
```

New:
```lua
hl.on("hyprland.start", function()
    hl.exec_cmd("waybar")
    hl.exec_cmd("nm-applet")
    hl.exec_cmd("waybar & hyprpaper & firefox")
end)
```

| Old | New |
|---|---|
| `exec-once = cmd` (runs once at startup) | `hl.on("hyprland.start", function() hl.exec_cmd("cmd") end)` |
| `exec = cmd` (runs every reload) | Call `hl.exec_cmd("cmd")` directly in file body (executes whenever the file is (re)loaded) |

---

## 12. Permissions (new in Lua era, optional)

```lua
hl.config({
    ecosystem = { enforce_permissions = true },
})

hl.permission("/usr/(bin|local/bin)/grim", "screencopy", "allow")
hl.permission("/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland", "screencopy", "allow")
hl.permission("/usr/(bin|local/bin)/hyprpm", "plugin", "allow")
```

`hl.permission(binary, type, mode)` — the three positional args map to the spec fields:

| Position | Field | Example values |
|---|---|---|
| 1st | `binary` | a regex matching the executable path, e.g. `"/usr/(bin\|local/bin)/grim"` |
| 2nd | `type` | the permission category, e.g. `"screencopy"`, `"plugin"`, `"keyboard"` |
| 3rd | `mode` | `"allow"`, `"deny"`, or `"ask"` |

No old hyprlang equivalent — this system (and `hyprland-guiutils` prompts) is new. Permission
changes require a Hyprland restart and are not applied on-the-fly, for security reasons.

---

## 13. Custom Layouts (new — no old equivalent)

```lua
hl.layout.register("columns", {
    recalculate = function(ctx)
        local n = #ctx.targets
        if n == 0 then return end
        for i, target in ipairs(ctx.targets) do
            target:place(ctx:column(i, n))
        end
    end,
})
-- used as: layout = "lua:columns"
```
Old hyprlang only shipped `dwindle` and `master`; writing a custom layout required a C++ plugin.
Lua configs can define one inline. `ctx` provides convenience functions like `grid_cell`,
`column`, `row`, `split`, plus `ctx.area` and `ctx.targets`.

---

## 14. Event Hooks (new — no old equivalent)

```lua
hl.on("window.active", function(w)
    hl.notification.create({ text = "Window focused: " .. w.title, timeout = 5000, icon = "ok" })
end)

hl.on("workspace.move_to_monitor", function(ws, m)
    hl.notification.create({
        text = "Workspace: " .. ws.name .. " moved to monitor at x: " .. m.position.x,
        timeout = 4000, icon = "ok",
    })
end)
```
Old hyprlang had no scripting/event system at all; this previously required external tools
(e.g. socket listeners on `hyprctl`).

`hl.on(event, fn)` returns an **event-subscription handle** (so a subscription can be managed
later). `hl.notification.create({...})` accepts `text` and `timeout` (required) plus optional
`color`, `icon` (integer id **or** string), and `font_size`; `hl.notification.get()` lists
active notifications. Event names come from Hyprland's internal event set — verify the exact
string (e.g. `"hyprland.start"`, `"window.active"`, `"workspace.move_to_monitor"`) against the
current wiki / `hl.meta.lua` stubs, since the list grows between releases.

---

## 15. Reading Config at Runtime (new)

```lua
hl.get_config("general.layout")   -- read current value of an option

-- example: toggle gaps_in between 0 and 3
hl.bind(mainMod .. " + SHIFT + G", function()
    local gapsInValueTable = hl.get_config("general.gaps_in")
    if gapsInValueTable.top == 3 then
        hl.config({ general = { gaps_in = 0 } })
    else
        hl.config({ general = { gaps_in = 3 } })
    end
end)
```
Equivalent old behavior required external `hyprctl getoption` shell calls; this is now native.
Note: return type of `hl.get_config()` mirrors the underlying value's structure (e.g. a 4-sided
spacing value comes back as a table with `top`/`bottom`/`left`/`right`-style keys).

---

## 16. Timers (new — no old equivalent)

```lua
local demoTimer = hl.timer(function()
    print("hello from timer")
end, { timeout = 1000, type = "repeat" })

-- demoTimer:set_enabled(false)
```

`hl.timer(callback, { timeout = ms, type = "repeat" | "oneshot" })` — `type` is `"repeat"` for a
recurring timer or **`"oneshot"`** for a single fire (not `"once"`). Both `timeout` and `type`
are required.

---

## 17. Complete Minimal Example (Lua) — Lua equivalent of the hyprlang minimal example

```lua
-- ~/.config/hypr/hyprland.lua

------------------
---- MONITORS ----
------------------
hl.monitor({ output = "", mode = "preferred", position = "auto", scale = "auto" })

---------------------
---- MY PROGRAMS ----
---------------------
local terminal = "kitty"
local fileManager = "dolphin"
local menu = "hyprlauncher"
local mainMod = "SUPER"

-------------------
---- AUTOSTART ----
-------------------
hl.on("hyprland.start", function()
    hl.exec_cmd("waybar")
    hl.exec_cmd("dunst")
    hl.exec_cmd("swww-daemon")
end)

-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------
hl.env("XCURSOR_SIZE", "24")

-----------------------
---- LOOK AND FEEL ----
-----------------------
hl.config({
    general = {
        gaps_in = 5,
        gaps_out = 10,
        border_size = 2,
        col = {
            active_border = { colors = {"rgba(33ccffee)", "rgba(00ff99ee)"}, angle = 45 },
            inactive_border = "rgba(595959aa)",
        },
        layout = "dwindle",
    },
    decoration = {
        rounding = 10,
        blur = { enabled = true, size = 3, passes = 1 },
        shadow = { enabled = true, range = 4 },
    },
    animations = { enabled = true },
})

hl.curve("easeOutQuint", { type = "bezier", points = { {0.23, 1}, {0.32, 1} } })
hl.curve("easy",         { type = "spring", mass = 1, stiffness = 71.2633, dampening = 15.8273644 })
hl.animation({ leaf = "windows",    enabled = true, speed = 4.79, spring = "easy" })
hl.animation({ leaf = "border",     enabled = true, speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "fade",       enabled = true, speed = 3.03, bezier = "default" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 1.94, bezier = "default", style = "fade" })

---------------
---- INPUT ----
---------------
hl.config({
    input = {
        kb_layout = "us",
        follow_mouse = 1,
        sensitivity = 0,
        touchpad = { natural_scroll = false },
    },
})

------------------
---- DWINDLE ----
------------------
hl.config({ dwindle = { preserve_split = true } })

---------------------
---- KEYBINDINGS ----
---------------------
hl.bind(mainMod .. " + Return", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + Q", hl.dsp.window.close())
hl.bind(mainMod .. " + M", hl.dsp.exit())
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + R", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))
hl.bind(mainMod .. " + F", hl.dsp.window.fullscreen({ mode = "fullscreen" }))

hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))

for i = 1, 5 do
    hl.bind(mainMod .. " + " .. i, hl.dsp.focus({ workspace = i }))
    hl.bind(mainMod .. " + SHIFT + " .. i, hl.dsp.window.move({ workspace = i }))
end

hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))

--------------------------------
---- WINDOW RULES ----
--------------------------------
hl.window_rule({
    name = "suppress-maximize-events",
    match = { class = ".*" },
    suppress_event = "maximize",
})

hl.window_rule({
    name = "float-pavucontrol",
    match = { class = "^(pavucontrol)$" },
    float = true,
})

hl.window_rule({
    name = "float-nm-editor",
    match = { class = "^(nm-connection-editor)$" },
    float = true,
})
```

---

## 18. Things With No Old Equivalent (purely new in Lua era)

- `hl.timer(fn, { timeout = ms, type = "repeat"/"oneshot" })` — schedule recurring/one-shot callbacks
- `hl.layout.register(name, {...})` — custom layouts written in Lua
- `hl.on(event, fn)` — event subscription system (returns a subscription handle)
- `hl.define_submap(name, reset_or_fn, fn?)` / `hl.get_current_submap()` — script-defined submaps
- `hl.get_config(path)` — read live config values from within scripts
- Runtime query API — `hl.get_windows()`, `hl.get_active_window()`, `hl.get_monitors()`,
  `hl.get_workspaces()`, `hl.get_cursor_pos()`, etc. (see §20)
- `hl.permission(path, perm, allow/deny)` and `ecosystem.enforce_permissions` — app permission prompts
- Bind/rule **handles** (`local b = hl.bind(...)`) with `:set_enabled(bool)` for runtime toggling
- `hl.gesture({...})` as a registrable, repeatable construct instead of fixed `workspace_swipe_*` options
- Native `require()` based file splitting with isolated error scopes per file (an error in one
  required file no longer breaks the whole config, unlike a syntax error anywhere in old
  hyprlang `.conf`, which could abort the entire reload)
- `decoration.rounding_power` — controls the corner-rounding curve shape, not present pre-0.55

---

## 19. Caveats for Feeding This to a Local LLM

- The Lua API is **actively evolving** post-0.55 (released 2026-05-09); exact key names
  (e.g. `no_blur` vs `noblur`, `ignore_alpha` casing) should be double-checked against
  `wiki.hypr.land` current pages or the in-repo Lua stubs (`meta/generateLuaStubs.py` output,
  typically installed to `/usr/share/hypr/stubs/`) before being treated as ground truth.
- `hl.dsp.*` dispatcher names in this doc are taken directly from the official example config
  (`example/hyprland.lua` in the `hyprwm/Hyprland` repo) — treat that file as the most
  authoritative living reference for exact dispatcher signatures.
- Where this doc says "verify exact key" it means the wiki text didn't give the literal Lua
  field name with full confidence — search `wiki.hypr.land` directly for that specific page
  rather than guessing from the old `.conf` name.

---

## 20. Runtime Query API (new — no old equivalent)

The Lua era exposes a full set of read-only getters for inspecting live compositor state from
within scripts/binds. Old hyprlang had none of this — the closest was shelling out to
`hyprctl clients -j` / `hyprctl monitors -j` and parsing JSON. These return live objects (with
`:` methods), not just plain tables.

```lua
local w  = hl.get_active_window()          -- HL.Window | nil
local ws = hl.get_active_workspace()       -- HL.Workspace | nil
local m  = hl.get_active_monitor()         -- HL.Monitor | nil

-- filtered / bulk queries
local windows = hl.get_windows({ ... })    -- HL.Window[]  (optional filter table)
local layers  = hl.get_layers({ ... })     -- HL.LayerSurface[]
```

| Function | Returns |
|---|---|
| `hl.get_windows(filters?)` | `HL.Window[]` |
| `hl.get_window(selector)` | `HL.Window \| nil` |
| `hl.get_active_window()` | `HL.Window \| nil` |
| `hl.get_urgent_window()` | `HL.Window \| nil` |
| `hl.get_last_window()` | `HL.Window \| nil` |
| `hl.get_workspaces()` | `HL.Workspace[]` |
| `hl.get_workspace(selector)` | `HL.Workspace \| nil` |
| `hl.get_active_workspace(monitor?)` | `HL.Workspace \| nil` |
| `hl.get_active_special_workspace(monitor?)` | `HL.Workspace \| nil` |
| `hl.get_workspace_windows(workspace)` | `HL.Window[]` |
| `hl.get_monitors()` | `HL.Monitor[]` |
| `hl.get_monitor(selector)` | `HL.Monitor \| nil` |
| `hl.get_active_monitor()` | `HL.Monitor \| nil` |
| `hl.get_monitor_at(x, y?)` / `hl.get_monitor_at_cursor()` | `HL.Monitor \| nil` |
| `hl.get_layers(filters?)` | `HL.LayerSurface[]` |
| `hl.get_cursor_pos()` | `HL.Vec2 \| nil` |
| `hl.get_config(key)` | current value of a config option (§15) |
| `hl.get_current_submap()` | `string` (active submap name) |

Selectors (`WindowSelector`, `WorkspaceSelector`, `MonitorSelector`) accept a string identifier,
an integer id, or an already-fetched object of the matching type. `hl.dispatch(dispatcher)` runs
a `hl.dsp.*` dispatcher imperatively (e.g. inside a multi-action bind function — see §4.3).