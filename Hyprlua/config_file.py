import pathlib
import dataclasses

@dataclasses.dataclass
class conf:
    
    home: pathlib.Path | str = pathlib.Path.home()
    
    @property
    def conf_file(self) -> pathlib.Path:
        path = pathlib.Path(self.home)
        path = path / ".config" / "hypr" / "hyprland.conf"
        return path
    
    @property
    def conf_dir(self) -> pathlib.Path :
        path = pathlib.Path(self.home)
        path = path / ".config" / "hypr"
        return path
        
    
if "__name__" == "__main__":
    c = conf()
    print(c.conf_dir)
    

