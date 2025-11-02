import gyc

def get_input() -> list[int]:
    return gyc.get_input()

def clear_screen() -> None:
    gyc.clear_screen()

def log(level: int, message: str) -> None:
    gyc.log(level, message)

def list_save() -> list[str]:
    return gyc.list_save()

def upload_save(key: str, value: str):
    gyc.upload_save(key, value)

def download_save(key: str) -> str | None:
    return gyc.download_save(key)

def delete_save(key: str) -> bool:
    return gyc.delete_save(key)

def load_asset(path: str) -> str:
    return gyc.load_asset(path)


from .base import VirtualKey

VKEY_NAMES = {
    VirtualKey.UP: '↑',
    VirtualKey.LEFT: '←',
    VirtualKey.DOWN: '↓',
    VirtualKey.RIGHT: '→',
    VirtualKey.F1: 'F1',
    VirtualKey.F2: 'F2',
    VirtualKey.F3: 'F3',
    VirtualKey.TAB: 'TAB',
    VirtualKey.OK: 'OK',
    VirtualKey.ALT: 'ALT',
}

KEY_MAPPING = {
    vkey: vkey
    for vkey, name in VKEY_NAMES.items()
}
