import parser
import config_file
import argparse


def show_help():
    print('''
    === HyprLua Config Manager ===
    
    Usage: hyprlua [command] [options]
    
    Commands:
      check          Check hyprlua configuration
      init           Initialize with auto-detection
      config [path]  View/parse configuration file
    
    Options:
      --help, -h     Show this help message
      --version, -v  Show version information
    ''')


def parse_arguments():
    parser = argparse.ArgumentParser(description='HyprLua Configuration Manager')
    parser.add_argument('--help', '-h', action='store_true', help='Show help and exit')
    parser.add_argument('--version', '-v', action='version', version='HyprLua 0.1')
    parser.add_argument('--config', '-c', dest='config_path', nargs='?', const='.', default=None,
                       help='Path to config directory (uses current dir if omitted)')
    parser.add_argument('command', nargs='?', default='check', choices=['check', 'init', 'config'],
                       help='Command to execute (default: check)')
    parser.add_argument('config_file', nargs='?', default=None, help='Path to config file (for config command)')
    
    return parser.parse_args()


def get_conf_dir(config_path=None):
    """Get configuration directory from CLI argument or auto-detection."""
    if config_path:
        conf = config_file.conf(config_path)
    else:
        conf = config_file.conf()
    
    return conf


def main():
    args = parse_arguments()
    
    if args.help:
        show_help()
        return
    
    # Get config directory from CLI argument or auto-detect
    conf = get_conf_dir(config_path=args.config_path)
    print('Using {} as config directory'.format(conf.conf_dir))
    
    if args.command == 'check':
        parser_args = parser.ConfigParser(config_dir=conf.conf_dir)
        config = parser_args.parse()
        print('Configuration loaded successfully!')
    
    elif args.command == 'init':
        print('Initialized using {} as conf dir'.format(conf.conf_dir))
    
    elif args.command == 'config':
        if args.config_file:
            print('Parsing config from: {}'.format(args.config_file))
            parser_args = parser.ConfigParser(config_dir=conf.conf_dir)
            config = parser_args.parse()
        else:
            parser_args = parser.ConfigParser(config_dir=conf.conf_dir)
            config = parser_args.parse()
            print('Configuration file: {}'.format(config_file.conf().conf_file))


if __name__ == '__main__':
    main()
