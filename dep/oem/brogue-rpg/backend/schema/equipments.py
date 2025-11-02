from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.item import *


class GearSlot[T: EquippableItem]:
    item: T | None
    index: int

    def __init__(self, index: int = 0):
        self.item = None
        self.index = index

    def is_empty(self) -> bool:
        return self.item is None
    
    def set(self, item: T) -> None:
        self.item = item
    

class Equipments:
    def __init__(self):
        self.headgear = GearSlot['Headgear'](0)
        self.armor = GearSlot['Armor'](1)
        self.weapon = GearSlot['Weapon'](2)
        self.accessories = [GearSlot['Accessory'](i) for i in range(3, 7)]
        self.wands = [GearSlot['Wand'](i) for i in range(7, 10)]

    def __iter__(self):
        yield self.headgear
        yield self.armor
        yield self.weapon
        yield from self.accessories
        yield from self.wands

    def __len__(self):
        return 3 + len(self.accessories) + len(self.wands)
