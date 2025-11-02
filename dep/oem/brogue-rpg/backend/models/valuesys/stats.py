import pickle as pkl
from .damage import *
from .common import ValueFix

class Stats:
    def __init__(self):
        self.MaxHP: int = 0
        self.MaxSP: int = 0
        
        self.Vit: int = 0       # 体质
        self.Str: int = 0       # 力量
        self.Int: int = 0       # 智力
        self.Spi: int = 0       # 精神
        self.Luk: int = 0       # 运气
        self.Unused: int = 0    # 未分配

        self.Hit: int = 0       # 命中
        self.Dodge: int = 0     # 闪避
        self.Block: int = 0     # 格挡

        self.dmg_types: dict[DamageTypeKey, ValueFix] = {
            'neutral': ValueFix(),
            'cold': ValueFix(),
            'fire': ValueFix(),
            'lightning': ValueFix(),
            'poison': ValueFix(),
            'curse': ValueFix(),
        }

        self.dmg_sources: dict[DamageSourceKey, ValueFix] = {
            'weapon': ValueFix(),
            'spell': ValueFix(),
            'debuff': ValueFix(),
        }

        self.dmg_methods: dict[DamageMethodKey, ValueFix] = {
            'melee': ValueFix(),
            'projectile': ValueFix(),
            'wave': ValueFix(),
            'transient': ValueFix(),
        }

    @property
    def Armor(self) -> int:
        return self.dmg_types['neutral'].reduction
    
    @Armor.setter
    def Armor(self, value: int) -> None:
        self.dmg_types['neutral'].reduction = value

    def copy(self) -> 'Stats':
        return pkl.loads(pkl.dumps(self))
    
    def ansi_colored_resist(self):
        cpnts = []
        for t, vfix in self.dmg_types.items():
            if t == 'neutral':
                continue
            val = round(vfix.reduction_pct * 100)
            t = DamageType.from_key(t)
            cpnts.append(t.color.ansi_fg(str(val)))
        return '/'.join(cpnts)
