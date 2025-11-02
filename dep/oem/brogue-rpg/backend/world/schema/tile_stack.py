from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .extras.fbm import FbmExtras
    from .region import RegionID

from .tile import Tile

class TileStack:
    region_id: 'RegionID'

    t_ground: Tile | None = None   # h=0.0，地面
    t_floor: Tile | None = None    # h=0.1，粘液
    t_plant: Tile | None = None    # h=0.5，植物
    t_block: Tile | None = None    # h=1.0，墙壁

    # 调试用的额外字段加在这里
    fbm_extras: FbmExtras | None = None

    def __init__(self):
        self.region_id = '?'

    def is_walkable(self) -> bool:
        if self.t_ground and not self.t_ground.is_walkable:
            return False
        if self.t_floor and not self.t_floor.is_walkable:
            return False
        if self.t_plant and not self.t_plant.is_walkable:
            return False
        if self.t_block and not self.t_block.is_walkable:
            return False
        return True