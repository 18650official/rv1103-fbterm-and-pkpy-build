import pickle as pkl
from vmath import vec2i
from array2d import chunked_array2d, array2d

from .tile_stack import TileStack
from .tile import AllTiles, Tile
from .region import Region, RegionID

class World:
    def __init__(self, chunk_size: int = 8) -> None:
        self.tiles = chunked_array2d[TileStack, None](chunk_size, default=TileStack())
        self.loaded_regions = dict[RegionID, Region]()

    def save_region(self, region_id: RegionID):
        region = self.loaded_regions[region_id]
        width, height = region.width, region.height
        mask = array2d[bool](width, height, default=False)
        t_ground = array2d[int](width, height, default=0)
        t_floor = array2d[int](width, height, default=0)
        t_plant = array2d[int](width, height, default=0)
        t_block = array2d[int](width, height, default=0)
        for pos, stack in region.tiles:
            mask[pos] = stack.region_id == region_id
            t_ground[pos] = 0 if stack.t_ground is None else stack.t_ground.id
            t_floor[pos] = 0 if stack.t_floor is None else stack.t_floor.id
            t_plant[pos] = 0 if stack.t_plant is None else stack.t_plant.id
            t_block[pos] = 0 if stack.t_block is None else stack.t_block.id
        return {
            'id': region_id,
            'width': width,
            'height': height,
            'nb_offsets': region.nb_offsets,
            'tiles': {
                'mask': mask,
                't_ground': t_ground,
                't_floor': t_floor,
                't_plant': t_plant,
                't_block': t_block,
            }
        }
    
    def load_region(self, data: dict | bytes):
        if not isinstance(data, dict):
            assert isinstance(data, bytes)
            data = pkl.loads(data)
            assert isinstance(data, dict)
        
        width: int = data['width']
        height: int = data['height']
        region_id: RegionID = data['id']
        nb_offsets: dict[RegionID, vec2i] = data['nb_offsets']
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert isinstance(region_id, str)

        if region_id in self.loaded_regions:
            raise ValueError(f"Region {region_id} already loaded")

        new_origin: vec2i

        if len(self.loaded_regions) == 0:
            new_origin = vec2i.ZERO
        else:
            if len(nb_offsets) == 0:
                raise ValueError("No neighbor regions specified for non-initial region")
            # 找到一个已经加载的邻居区域
            for nb_id, offset in nb_offsets.items():
                if nb_id in self.loaded_regions:
                    nb_region = self.loaded_regions[nb_id]
                    new_origin = nb_region.origin - offset
                    break
            else:
                raise ValueError("No loaded neighbor region found")

        new_region = Region(
            id=region_id,
            origin=new_origin,
            width=width,
            height=height,
            nb_offsets=nb_offsets,
            tiles=self.tiles.view_rect(
                new_origin,
                width,
                height
            )
        )

        mask: array2d[bool] = data['tiles']['mask']
        t_ground: array2d[int] = data['tiles']['t_ground']
        t_floor: array2d[int] = data['tiles']['t_floor']
        t_plant: array2d[int] = data['tiles']['t_plant']
        t_block: array2d[int] = data['tiles']['t_block']

        new_region.tiles.apply(lambda _: TileStack())
        for pos, stack in new_region.tiles:
            if mask[pos]:
                stack.region_id = region_id
                stack.t_ground = AllTiles.get(t_ground[pos])
                stack.t_floor = AllTiles.get(t_floor[pos])
                stack.t_plant = AllTiles.get(t_plant[pos])
                stack.t_block = AllTiles.get(t_block[pos])

        self.loaded_regions[region_id] = new_region
        return new_region
