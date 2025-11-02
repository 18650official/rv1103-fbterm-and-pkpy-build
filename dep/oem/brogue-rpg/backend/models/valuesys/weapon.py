from typing import Literal
from .common import Enum

WeaponTypeKey = Literal[
    'sword', 'axe', 'dagger', 'hammer', 'club', 'spear', 'staff', 'shield',
    'bow', 'gun', 'thrown'
    ]
class WeaponType(Enum[WeaponTypeKey]):
    def __init__(self, key: WeaponTypeKey, is_melee: bool):
        super().__init__(key)
        self.is_melee = is_melee

WeaponType('sword', True)
WeaponType('axe', True)
WeaponType('dagger', True)
WeaponType('hammer', True)
WeaponType('club', True)
WeaponType('spear', True)
WeaponType('staff', True)
WeaponType('shield', True)

WeaponType('bow', False)
WeaponType('gun', False)
WeaponType('thrown', False)
