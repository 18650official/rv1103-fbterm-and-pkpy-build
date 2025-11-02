from dataclasses import dataclass
from typing import TYPE_CHECKING
from vmath import vec2i

if TYPE_CHECKING:
    from ..tile import TileID

@dataclass
class GeoCell:
    position: vec2i  # 坐标
    altitude: float  # 海拔(m)
    solar_radiation: float  # 太阳辐射(MJ/m^2/year)
    temperature: float  # 温度(℃)
    humidity: float  # 湿度(%)
    wind_speed: float  # 风速(m/s)
    wind_direction: float  # 风向(°)正北方向吹来的风为0°
    precipitation: float  # 降水量(mm)
    slope: float  # 坡度(°)
    aspect: float  # 朝向(°)山脚指向山顶的方向

@dataclass
class TerrainCell:
    position: vec2i
    ground_tile_id: TileID
    env_obj_seed: 'EnvironmentObjectSeed | None'
    structure_seed: 'StructureSeed | None'
    
@dataclass
class EnvironmentObjectSeed:
    env_obj_id: TileID
    shape: vec2i
    
@dataclass
class StructureSeed:
    structure_id: TileID
    shape: vec2i

@dataclass
class FbmExtras:
    geo_cell: GeoCell
    terrain_cell: TerrainCell
    env_seed: EnvironmentObjectSeed
    structure_seed: StructureSeed