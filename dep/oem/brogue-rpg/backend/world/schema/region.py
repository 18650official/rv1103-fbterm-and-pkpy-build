from typing import TYPE_CHECKING
from dataclasses import dataclass
from vmath import vec2i
from array2d import array2d_view

if TYPE_CHECKING:
    from .tile_stack import TileStack

RegionID = str

@dataclass
class Region:
    id: RegionID
    origin: vec2i
    width: int
    height: int
    nb_offsets: dict[RegionID, vec2i]
    tiles: array2d_view[TileStack]
