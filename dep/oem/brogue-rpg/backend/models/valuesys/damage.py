from vmath import color32, rgb
from typing import Literal
from .common import Enum

DamageTypeKey = Literal['neutral', 'fire', 'cold', 'lightning', 'poison', 'curse']
class DamageType(Enum[DamageTypeKey]):
    def __init__(self, key: DamageTypeKey, icon: str, color: color32, is_elemental: bool):
        super().__init__(key)
        self.icon = icon
        self.color = color
        self.is_elemental = is_elemental

DamageType('neutral', '✨', rgb(255, 255, 255), False)
DamageType('fire', '🔥', rgb(255, 100, 0), True)
DamageType('cold', '❄️', rgb(100, 100, 255), True)
DamageType('lightning', '⚡', rgb(255, 255, 0), True)
DamageType('poison', '🫧', rgb(0, 200, 0), False)
DamageType('curse', '🌀', rgb(160, 0, 160), False)


DamageSourceKey = Literal['weapon', 'spell', 'debuff']
class DamageSource(Enum[DamageSourceKey]):
    def __init__(self, key: DamageSourceKey):
        super().__init__(key)

DamageSource('weapon')
DamageSource('spell')
DamageSource('debuff')


DamageMethodKey = Literal['melee', 'projectile', 'wave', 'transient']
class DamageMethod(Enum[DamageMethodKey]):
    def __init__(self, key: DamageMethodKey):
        super().__init__(key)

DamageMethod('melee')
DamageMethod('projectile')
DamageMethod('wave')
DamageMethod('transient')


class DamageInfo:
    type: DamageTypeKey
    source: DamageSourceKey
    method: DamageMethodKey

    def __init__(self, type: DamageTypeKey, source: DamageSourceKey, method: DamageMethodKey):
        self.type = type
        self.source = source
        self.method = method
