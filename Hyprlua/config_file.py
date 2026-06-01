import pathlib
import dataclasses

@dataclasses.dataclass
class Conf:

    _config: pathlib.Path | str = None

    @property
    def config(self) -> pathlib.Path:
        if self._config is None:
            return pathlib.Path(pathlib.Path.home()) / ".config"
        else:
            if isinstance(self._config, str):
                return pathlib.Path(self._config)
            else:
                return self._config
    
    @property
    def conf_file(self) -> pathlib.Path:
        return self.config / "hypr" / "hyprland.conf"
    
    @property
    def conf_dir(self) -> pathlib.Path :
        return self.config / "hypr"

    

