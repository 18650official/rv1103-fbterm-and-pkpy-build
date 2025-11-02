from .base import Actor, PRIORITY_MOB
from ..valuesys import ActorType, ActorTypeKey

class Mob(Actor):
    def __init__(self) -> None:
        super().__init__()
        self.level = 0
        self.tb_info.priority = PRIORITY_MOB

    @property
    def char(self) -> str:
        return '👹'
    
    @property
    def is_mob(self) -> bool:
        return True
    
    def with_level(self, level: int, type: ActorTypeKey):
        assert level >= 1
        self.level = level

        # level = range(1, 31)
        self.base_stats.MaxHP = formula(1 + level * 3)
        self.base_stats.MaxSP = 0

        self.base_stats.Dodge = formula(round(level * 0.25))
        self.base_stats.Block = 0

        self.base_stats.Armor = formula(level - 1)

        # 应用major type修正
        ActorType.from_key(type).stats_fix.apply(self.base_stats)

        self.update_stats()
        self.hp = self.stats.MaxHP
        return self
