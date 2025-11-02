from vmath import vec3i, color32

class AsciiSprite:
    def __init__(self, char: str, fg: str | None = None, bg: str | None = None):
        self.char = char
        self.fg = color32.from_hex(fg) if fg else None
        self.bg = color32.from_hex(bg) if bg else None

class Tileset:
    def __init__(self, id: int, sprites: list[AsciiSprite]):
        self.id = id
        self.sprites = sprites


class TilesetId:
    Chasm = 0
    Water = 1
    Ground = 2
    Floor = 3
    Slime = 4
    Grass = 5
    Fire = 6
    Wall = 7
    Tree = 8


_db = [
    # 裂隙
    Tileset(TilesetId.Chasm, [
        AsciiSprite('　'),
    ]),
    # 水
    Tileset(TilesetId.Water, [
        AsciiSprite('　', bg="#00aaff"),
    ]),
    # 地基
    Tileset(TilesetId.Ground, [
        AsciiSprite('・'),
        AsciiSprite('・', bg="#314c6e"),
    ]),
    # 地板
    Tileset(TilesetId.Floor, [
        AsciiSprite('＊'),
    ]),
    # 粘液
    Tileset(TilesetId.Slime, [
        AsciiSprite('～', bg="#ff44ef"),
    ]),
    # 草
    Tileset(TilesetId.Grass, [
        AsciiSprite('🌿'),
    ]),
    # 火焰
    Tileset(TilesetId.Fire, [
        AsciiSprite('🔥', bg="#ff6229"),
    ]),
    # 墙体
    # https://unicode.party/?query=mountain
    Tileset(TilesetId.Wall, [
        AsciiSprite('🧱'),
        AsciiSprite('🪨'),
        AsciiSprite('🧊'),
        AsciiSprite('⛰️'),
        AsciiSprite('🏔️'),
        AsciiSprite('🗻'),
        AsciiSprite('🌋'),
    ]),
    # 树木
    # https://unicode.party/?query=tree
    Tileset(TilesetId.Tree, [
        AsciiSprite('🌲'),
        AsciiSprite('🎄'),
        AsciiSprite('🌴'),
        AsciiSprite('🎋'),
        AsciiSprite('🌳'),
    ]),
]

def get_sprite(tileset_id: int, index: int) -> AsciiSprite:
    return _db[tileset_id].sprites[index]
