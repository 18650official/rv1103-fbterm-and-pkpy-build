import sys
from vmath import vec2i

from .base import VirtualKey

if sys.platform in ['win32', 'darwin', 'linux']:
    from . import desktop as _platform
else:
    from . import gyc as _platform

get_input = _platform.get_input
log = _platform.log
list_save = _platform.list_save
upload_save = _platform.upload_save
download_save = _platform.download_save
delete_save = _platform.delete_save
load_asset = _platform.load_asset
clear_screen = _platform.clear_screen
KEY_MAPPING = _platform.KEY_MAPPING
VKEY_NAMES = _platform.VKEY_NAMES


class Input:
    def __init__(self):
        self.state = [False] * VirtualKey.__count__
        self.any_key_down = False
        self.axis = vec2i.ZERO

        self.axis_mapping = {
            VirtualKey.UP: vec2i(0, -1),
            VirtualKey.DOWN: vec2i(0, 1),
            VirtualKey.LEFT: vec2i(-1, 0),
            VirtualKey.RIGHT: vec2i(1, 0),
        }

    def vkey_name(self, vkey: int) -> str:
        return '[' + VKEY_NAMES[vkey] + ']'

    def update(self):
        for i in range(len(self.state)):
            self.state[i] = False
        self.any_key_down = False
        self.axis = vec2i.ZERO

        for key in get_input():
            vkey = KEY_MAPPING.get(key)
            if vkey is not None:
                if not self.state[vkey]:    # 有时一帧会报两个重复key
                    self.axis += self.axis_mapping.get(vkey, vec2i.ZERO)
                self.state[vkey] = True
                self.any_key_down = True

    def wait_for_input(self):
        yield
        while not self.any_key_down:
            yield
        return self.state.copy(), self.axis

