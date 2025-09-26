from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING
from vmath import vec2i

from backend.asyncio import *

from ..stats import Stats
from ..affix import AffixGroup, Trigger
from ..buff import Buff


if TYPE_CHECKING:
    from backend.battle.attack import IWeapon

PRIORITY_VFX = 100          # visual effects take priority
PRIORITY_HERO = 0           # positive is before hero, negative after
PRIORITY_BLOB = -10         # blobs act after hero, before mobs
PRIORITY_MOB = -20          # mobs act between buffs and blobs
PRIORITY_BUFF = -30         # buffs act last in a turn
PRIORITY_DEFAULT = -100     # if no priority is given, act after all else

@dataclass
class TurnBasedInfo:
    time: float = 0.0                   # 时间轴计数
    priority: int = PRIORITY_DEFAULT    # 回合优先级

class TurnBasedActor(Protocol):
    tb_info: TurnBasedInfo
    def wait_for_command(self) -> Task | Future[Task]: ...

class Actor:
    def __init__(self):
        self.tb_info = TurnBasedInfo()

        self.stats = Stats()
        self.buffs = []            # type: list[Buff]
        self.talents = AffixGroup()

        self.level = 0
        self.hp = 0
        self.sp = 0
        self.shield = 0
        self.pos = vec2i(0, 0)          # 坐标
        self.facing = vec2i(0, 0)       # 朝向

        self.bigworld_loading_radius = 0

    @property
    def hp_vec2i(self) -> vec2i:
        return vec2i(self.hp, self.stats.max_hp.value)
    
    @property
    def sp_vec2i(self) -> vec2i:
        return vec2i(self.sp, self.stats.max_sp.value)

    def add_hp(self, value: int) -> None:
        value = self.hp + value
        if value < 0:
            value = 0
        self.hp = min(value, self.stats.max_hp.value)

    def add_sp(self, value: int) -> None:
        value = self.sp + value
        if value < 0:
            value = 0
        self.sp = min(value, self.stats.max_sp.value)
    
    @property
    def is_hero(self) -> bool:
        return False
    
    @property
    def is_mob(self) -> bool:
        return False
    
    @property
    def char(self) -> str:
        raise NotImplementedError(type(self))
    
    @property
    def normal_attack(self) -> IWeapon | None:
        raise NotImplementedError(type(self))
    
    def face_direction(self, delta: vec2i) -> None:
        if delta.x != 0 and delta.y != 0:
            delta = delta.with_y(0)
        self.facing = delta

    def interact(self, actor: 'Actor') -> Task | None:
        return
    
    def wait_for_command(self) -> Task | Future[Task]:
        raise NotImplementedError(type(self))
    
    def update_stats(self):
        self.stats.reset()
        for buff in self.buffs:
            buff.affixes.apply_modifiers(self.stats, 'from_buff')
        self.talents.apply_modifiers(self.stats, 'from_talent')

    def collect_triggers(self):
        triggers: list[Trigger] = []
        for buff in self.buffs:
            triggers.extend(buff.affixes.triggers)
        for talent in self.talents.triggers:
            triggers.append(talent)
        return triggers
