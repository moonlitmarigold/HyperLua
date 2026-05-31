#from pathlib import Path
import parser
import config_file

def ask_home():
    conf = config_file.conf()
    
    answer = input('Use {} as config path? (y/n):'.format(conf.conf_dir))
    
    if answer.lower() == "n":
        new_conf = input('Enter custom path to hyprland config dir:')
        
        conf = config_file.conf(new_conf)
    
    return conf
        



# Ask for conf dir
conf = ask_home()

print('Now using {} as conf dir'.format(conf.conf_dir))
    
parser.main(conf.conf_dir)