from typing import Self
import pickle as pkl

from backend.models.affix import AffixGroup

class Spell:
    def copy(self) -> Self:
        return pkl.loads(pkl.dumps(self))

class PrimarySpell(Spell):
    cast_delay: float
    recharge_time: float
    hit_rate: int
    crit_rate: int

    uses: int
    mana_cost: int
    sp_cost: int
    radius: int
    damage: int

class WandPassive(Spell):
    affixes: AffixGroup

class SpellBoost(Spell):
    affixes: AffixGroup

class SpellGroup:
    spell: PrimarySpell
    indices: list[int]

    def __init__(self, spell: PrimarySpell, indices: list[int]):
        assert isinstance(spell, PrimarySpell)
        self.spell = spell
        self.indices = indices
