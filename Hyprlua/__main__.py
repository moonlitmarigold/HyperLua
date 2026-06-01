from . import config_file
import argparse


def show_help():
    print('''
    =======  HyprLua  =======
    
    Usage: hyprlua [options]
    
    Simple tool to update old Hyprland configs to the new Lua format.
    Updated configs will be placed in the same directory as the original config by default, but you can specify a custom output file with the --output option.
    
    Options:
      --help, -h     Show this help message
      --version, -v  Show version information
      --config, -c   Path to config directory (uses standard ~/.config if omitted)
      --output, -o   Custom output file (defaults to placing files in the same directory as the original config)
    ''')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple tool to update old Hyprland configs to the new Lua format.\nUpdated configs will be placed in the same directory as the original config by default, but you can specify a custom output file with the --output option.', add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('--version', '-v', action='version', version='HyprLua 0.1')
    parser.add_argument('--config', '-c', dest='config_path', nargs='?',  default=None,
                        help='Path to config directory (uses standard ~/.config if omitted)')
    parser.add_argument('--output', '-o',  dest='output_path', nargs='?', default=None,
                        help='Custom output file (defaults to placing files in the same directory as the original config)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.help:
        show_help()
        return
    
    # Get config directory from CLI argument or auto-detect
    conf = config_file.Conf(args.config_path)
    print('Using {} as Hyprland config directory'.format(conf.conf_dir))

    return


if __name__ == '__main__':
    main()
