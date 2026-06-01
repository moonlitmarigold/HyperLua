import dataclasses
import logging
from pathlib import Path
logger = logging.getLogger('HyprLua')

@dataclasses.dataclass
class EmptyLine:
    ...

@dataclasses.dataclass
class Base:
    keyword:str
    content:str = ''

REGISTRY: list = list()

def register(cls):
    REGISTRY.append(cls)
    return cls  # must return cls so the class still works normally

@register
@dataclasses.dataclass
class File(Base):
    name: str
    location:Path
    hyprland_location:Path
    keyword = 'source'
    lines:list = dataclasses.field(default_factory=list)

@register
@dataclasses.dataclass
class Comment(Base):
    keyword = '#'

@register
@dataclasses.dataclass
class Monitor(Base):
    keyword = 'monitor'