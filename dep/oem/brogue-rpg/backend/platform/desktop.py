import os
from conio import _kbhit, _getch

from .base import VirtualKey

def get_input() -> list[int]:
    keys = []
    while _kbhit():
        keys.append(_getch())
    return keys

def clear_screen():
    print('\x1b[H\x1b[J', end='')

def log(level: int, message: str):
    pass

def list_save() -> list[str]:
    if not os.path.exists("save"):
        return []
    return os.listdir("save")

def upload_save(key: str, value: str):
    if not os.path.exists("save"):
        os.mkdir("save")
    with open(f"save/{key}", "w") as f:
        f.write(value)

def download_save(key: str) -> str | None:
    filename = f"save/{key}"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()

def delete_save(key: str) -> bool:
    filename = f"save/{key}"
    if os.path.exists(filename):
        os.remove(filename)
        return True
    return False

def load_asset(path: str) -> str:
    with open(path, "rt") as f:
        return f.read()

KEY_MAPPING = {
    ord('w'): VirtualKey.UP, ord('W'): VirtualKey.UP,
    ord('a'): VirtualKey.LEFT, ord('A'): VirtualKey.LEFT,
    ord('s'): VirtualKey.DOWN, ord('S'): VirtualKey.DOWN,
    ord('d'): VirtualKey.RIGHT, ord('D'): VirtualKey.RIGHT,
    ord('1'): VirtualKey.F1,
    ord('2'): VirtualKey.F2,
    ord('3'): VirtualKey.F3,
    9: VirtualKey.TAB,
    ord(' '): VirtualKey.OK,
    ord('z'): VirtualKey.ALT, ord('Z'): VirtualKey.ALT,
}

VKEY_NAMES = {
    VirtualKey.UP: 'W',
    VirtualKey.LEFT: 'A',
    VirtualKey.DOWN: 'S',
    VirtualKey.RIGHT: 'D',
    VirtualKey.F1: '1',
    VirtualKey.F2: '2',
    VirtualKey.F3: '3',
    VirtualKey.TAB: 'TAB',
    VirtualKey.OK: 'SPACE',
    VirtualKey.ALT: 'Z',
}
