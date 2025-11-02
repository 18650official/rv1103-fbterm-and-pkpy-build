from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from .stats import Stats

from .damage import DamageTypeKey
from .common import Enum

@dataclass
class StatsFix:
    max_hp: float = 0.0
    armor: float = 0.0
    dodge: float = 0.0
    weapon_dmg: float = 0.0
    spell_dmg: float = 0.0
    resist: dict[DamageTypeKey, float] | None = None

    def apply(self, stats: 'Stats'):
        stats.MaxHP += round(stats.MaxHP * (1 + self.max_hp))
        stats.Armor += round(stats.Armor * (1 + self.armor))
        stats.Dodge += round(stats.Dodge * (1 + self.dodge))
        stats.dmg_sources['weapon'].boost_pct += self.weapon_dmg
        stats.dmg_sources['spell'].boost_pct += self.spell_dmg

        if self.resist is not None:
            for k, v in self.resist.items():
                stats.dmg_types[k].reduction_pct += v


ActorTypeKey = Literal['humanioid', 'beast', 'undead', 'construct', 'spellbeast', 'ethereal']
class ActorType(Enum[ActorTypeKey]):
    def __init__(self, key: ActorTypeKey, stats_fix: StatsFix):
        super().__init__(key)
        self.stats_fix = stats_fix

ActorType('humanioid', StatsFix(
    resist={
        'curse': -0.50,
    }
))
ActorType('beast', StatsFix(
    max_hp=0.30,
    armor=0.20,
    dodge=-0.10,
    weapon_dmg=0.25,
    spell_dmg=-0.40,
    resist={
        'fire': -0.25,
        'poison': -0.25,
        'curse': -0.25,
    }
))
ActorType('undead', StatsFix(
    max_hp=0.15,
    armor=0.25,
    dodge=-0.20,
    weapon_dmg=0.10,
    spell_dmg=0.10,
    resist={
        'fire': -0.25,
        'cold': 0.25,
        'lightning': -0.10,
        'poison': 0.25,
    }
))
ActorType('construct', StatsFix(
    max_hp=0.40,
    armor=0.50,
    dodge=-0.40,
    weapon_dmg=0.15,
    spell_dmg=-0.40,
    resist={
        'lightning': 0.10,
        'poison': 0.50,
    }
))
ActorType('spellbeast', StatsFix(
    max_hp=0.10,
    armor=-0.10,
    dodge=0.10,
    weapon_dmg=-0.20,
    spell_dmg=0.50,
    resist={
        'cold': -0.25,
        'poison': -0.10,
        'curse': -0.25,
    }
))
ActorType('ethereal', StatsFix(
    max_hp=-0.20,
    armor=-0.30,
    dodge=0.40,
    weapon_dmg=-0.50,
    spell_dmg=0.30,
    resist={
        'fire': -0.25,
        'cold': -0.25,
        'lightning': -0.25,
        'curse': -0.25,
    }
))
