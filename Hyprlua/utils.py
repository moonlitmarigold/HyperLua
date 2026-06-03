

def add_comment(line:str):
    if line.startswith('#'):
        return line
    else:
        return '#' + ' ' + line