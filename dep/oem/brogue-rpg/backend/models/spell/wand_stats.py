from dataclasses import dataclass
from typing import Self
import pickle as pkl

@dataclass
class WandStats:
    mana_max: int           # 最大法力值
    mana_regen: int         # 每回合恢复的法力值
    capacity: int           # 法杖容量，可以放多少格法术

    cast_delay: float       # 释放完一个法术组后，等待多少回合才能释放下一个法术组
    recharge_time: float    # 所有法术组释放完后，等待多少回合才会刷新
    hit_rate: int           # 命中率
    crit_rate: int          # 暴击率

    def copy(self) -> Self:
        return pkl.loads(pkl.dumps(self))
