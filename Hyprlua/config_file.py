import pathlib
import dataclasses

@dataclasses.dataclass
class ConfExtraFile:

    config_file: pathlib.Path

    @property
    def conf_file(self) -> pathlib.Path:
        return self.config_file

    @property
    def conf_dir(self) -> pathlib.Path:
        return self.config_file.parent

@dataclasses.dataclass
class Conf:

    _config: pathlib.Path | str = None

    @property
    def config(self) -> pathlib.Path:
        if self._config is None:
            return pathlib.Path(pathlib.Path.home()) / ".config" / "hypr"
        else:
            if isinstance(self._config, str):
                return pathlib.Path(self._config).expanduser()
            else:
                return self._config.expanduser()
    
    @property
    def conf_file(self) -> pathlib.Path:
        return self.config / "hyprland.conf"
    
    @property
    def conf_dir(self) -> pathlib.Path :
        return self.config