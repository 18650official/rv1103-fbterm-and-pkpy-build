from vmath import color32, rgb, rgba
from dataclasses import dataclass
from typing import Literal

TileID = int
TileLayer = Literal['t_ground', 't_floor', 't_plant', 't_block', '']

@dataclass
class Tile:
    id: TileID
    layer: TileLayer
    name: str
    char: str
    fg: color32 | None
    bg: color32 | None

    tags: list[str]
    is_walkable: bool

    def is_void(self):
        return self.id == 0


AllTiles: dict[TileID, Tile] = {}

# https://hclcat.games/3rd/grist/sql?q=select%20*%20from%20tile

null = None
_raw_tile_table_data = {"statement":"select * from tile","records":[{"fields":{"id":1,"manualSort":1,"id2":1,"layer":"t_ground","char":"・","fg":"","bg":"","tags":null,"is_walkable":1,"name":"粘土地面（主）"}},{"fields":{"id":2,"manualSort":2,"id2":2,"layer":"t_ground","char":"，","fg":"","bg":"","tags":null,"is_walkable":1,"name":"岩石地面（次）"}},{"fields":{"id":3,"manualSort":3,"id2":3,"layer":"t_ground","char":"〜","fg":"","bg":"#009dee","tags":null,"is_walkable":0,"name":"水"}},{"fields":{"id":4,"manualSort":4,"id2":25,"layer":"t_floor","char":"　","fg":"","bg":"#ff780080","tags":null,"is_walkable":1,"name":"粘液表层"}},{"fields":{"id":5,"manualSort":5,"id2":50,"layer":"t_plant","char":"🌿","fg":"","bg":"","tags":null,"is_walkable":1,"name":"草"}},{"fields":{"id":6,"manualSort":6,"id2":51,"layer":"t_plant","char":"🌼","fg":"","bg":"","tags":null,"is_walkable":1,"name":"花"}},{"fields":{"id":7,"manualSort":7,"id2":52,"layer":"t_plant","char":"🪨","fg":"","bg":"","tags":null,"is_walkable":0,"name":"石块"}},{"fields":{"id":8,"manualSort":8,"id2":53,"layer":"t_plant","char":"🔥","fg":"","bg":"","tags":null,"is_walkable":1,"name":"火焰"}},{"fields":{"id":9,"manualSort":9,"id2":54,"layer":"t_plant","char":"🌲","fg":"","bg":"","tags":null,"is_walkable":0,"name":"树"}},{"fields":{"id":10,"manualSort":10,"id2":75,"layer":"t_block","char":"🧱","fg":"","bg":"","tags":null,"is_walkable":0,"name":"粘土墙壁（主）"}},{"fields":{"id":11,"manualSort":11,"id2":76,"layer":"t_block","char":"🟫","fg":"","bg":"","tags":null,"is_walkable":0,"name":"岩石墙壁（次）"}},{"fields":{"id":12,"manualSort":12,"id2":77,"layer":"t_block","char":"🚪","fg":"","bg":"","tags":null,"is_walkable":0,"name":"关闭的门"}},{"fields":{"id":13,"manualSort":13,"id2":78,"layer":"t_block","char":"＋","fg":"","bg":"","tags":null,"is_walkable":1,"name":"打开的门"}},{"fields":{"id":14,"manualSort":14,"id2":200,"layer":"t_block","char":"📦","fg":"","bg":"","tags":null,"is_walkable":0,"name":"箱子"}},{"fields":{"id":15,"manualSort":15,"id2":201,"layer":"t_block","char":"👦","fg":"","bg":"","tags":null,"is_walkable":0,"name":"NPC"}},{"fields":{"id":16,"manualSort":9.5,"id2":55,"layer":"t_plant","char":"🕯️","fg":"","bg":"","tags":null,"is_walkable":0,"name":"火把"}},{"fields":{"id":17,"manualSort":16,"id2":202,"layer":"t_block","char":"🔮","fg":"","bg":"","tags":null,"is_walkable":0,"name":"传送门"}}]}

for row in _raw_tile_table_data['records']:
    fields = row['fields']
    tile_id = fields['id2']
    layer = fields['layer']
    name = fields['name']
    char = fields['char']
    fg = color32.from_hex(fields['fg']) if fields['fg'] else None
    bg = color32.from_hex(fields['bg']) if fields['bg'] else None
    tags = fields['tags']
    is_walkable = bool(fields['is_walkable'])

    AllTiles[tile_id] = Tile(tile_id, layer, name, char, fg, bg, tags, is_walkable)
