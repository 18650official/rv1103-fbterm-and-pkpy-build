import math

from .base import Actor, PRIORITY_HERO

class Hero(Actor):
    def __init__(self) -> None:
        super().__init__()

        self.level = 1
        self.exp = 0

        self.hp = 5
        self.sp = 0

        self.base_stats.MaxHP = 20
        self.base_stats.MaxSP = 10
        self.base_stats.Unused = 1

        self.tb_info.priority = PRIORITY_HERO

        self.bigworld_loading_radius = 2

        from backend.schema.inventory import Inventory
        from backend.schema.equipments import Equipments
        self.inventory = Inventory()
        self.equipments = Equipments()

        self.update_stats()

    def next_level_exp(self) -> int:
        # self.level = range(1, 30)
        return formula(round(742 * math.log((self.level-1)*0.2+1) + 100))

    @property
    def is_hero(self) -> bool:
        return True
    
    @property
    def char(self) -> str:
        return '🧙'
    
    def act(self, context: dict):
        return current_io().wait_for_input_and_act(context)
    
    def update_stats(self):
        super().update_stats()
        for slot in self.equipments:
            if slot.item is not None:
                slot.item.affixes.apply_modifiers(self.stats)

    def collect_triggers(self):
        triggers = super().collect_triggers()
        for slot in self.equipments:
            if slot.item is not None:
                triggers.extend(slot.item.affixes.triggers)
        return triggers

