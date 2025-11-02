from typing import Literal
from .common import Enum

ArmorTypeKey = Literal['light', 'medium', 'heavy']
class ArmorType(Enum[ArmorTypeKey]):
    def __init__(self, key: ArmorTypeKey):
        super().__init__(key)

ArmorType('light')
ArmorType('medium')
ArmorType('heavy')

