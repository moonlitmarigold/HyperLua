# HyperLua
Custom Python Parser to Update the old hyprland config files to the new lua version.

## Installation

```bash
git clone https://github.com/moonlitmarigold/HyperLua.git
cd HyperLua
python -m HyperLua
```

## Usage
```
--help, -h     Show a help message
--version, -v  Show version information
--config, -c   Path to Hyprland config directory (uses standard ~/.config/hypr if omitted)
--output, -o   Custom output file (defaults to placing files in the same directory as the original config)
--debug, -d    Show debug information
```

## Disclaimer (Read before Usage)

This tool is provided as-is, without any warranty. Use it at your own risk.
Not everything in the old syntax will be converted perfectly/is not supported (layerrules, binds and gestures), and some manual adjustments may be necessary after conversion. 
It is recommended to generate the files in a separate directory and then manually fix any issues before replacing your original config files.