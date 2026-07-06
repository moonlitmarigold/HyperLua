from . import config_file
from . import parser, build
import argparse
from pathlib import Path
import logging


def show_help():
    print('''
    =======  HyprLua  =======
    
    Usage: hyprlua [options]
    
    Simple tool to update old Hyprland configs to the new Lua format.
    Updated configs will be placed in the same directory as the original config by default, but you can specify a custom output file with the --output option.
    
    Options:
      --help, -h     Show this help message
      --config, -c   Path to Hyprland config directory (uses standard ~/.config/hypr if omitted)
      --output, -o   Custom output file (defaults to placing files in the same directory as the original config)
      --debug, -d    Show debug information
    ''')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple tool to update old Hyprland configs to the new Lua format.\nUpdated configs will be placed in the same directory as the original config by default, but you can specify a custom output file with the --output option.', add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')
    parser.add_argument('--config', '-c', dest='config_path', nargs='?',  default=None,
                        help='Path to Hyprland config directory (uses standard ~/.config/hypr if omitted)')
    parser.add_argument('--output', '-o',  dest='output_path', nargs='?', default=None,
                        help='Custom output file (defaults to placing files in the same directory as the original config)')
    parser.add_argument('--debug', '-d', action='store_true', help='Show debug information')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.help:
        show_help()
        return
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    conf = config_file.Conf(args.config_path)

    if args.output_path is None:
        output = conf
    else:
        output = config_file.ConfExtraFile(Path(args.output_path).expanduser())

    print('Using {} as Hyprland config directory, and {} as the config file'.format(conf.conf_dir, conf.conf_file))
    print('Using {} as output directory'.format(output.conf_dir))
    print('')

    # Inform User before starting the script
    print('This script will update part of your Hyprland config files to the new Lua format. Since not everything is supported (especially binds) or the potential of wrong translations, it is highly discouraged use the automatically translated config files directly, AS IT MAY BREAK YOUR SYSTEM.')
    print('Please try to use another config path outside your current hyprland file and correct any wrong or unsupported syntax before using the translated files. Any unsupported syntax will be commented.')
    print('Currently layerrules, gestures and binds are not fully supported.')
    response = input('Do you want to continue? (y/n): ')
    if response.lower() != 'y':
        return
    # Get config directory from CLI argument or auto-detect
    File = parser.Parser(conf).start_parser()

    build.Builder(conf, output).build(File)
    return


if __name__ == '__main__':
    main()
