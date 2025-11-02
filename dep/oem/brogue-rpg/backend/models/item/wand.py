from vmath import vec2i

from backend.models.affix import AffixGroup
from backend.models.spell import *
from backend.models.effect import Effect

from .base import EquippableItem, Item


class CompiledWand:
    def __init__(self, stats: WandStats):
        self.stats = stats
        self.index: int = 0
        self.spell_groups: list[SpellGroup] = []


class Wand(EquippableItem):
    def __init__(
            self,
            name: String | None = None,
            icon: str | None = None,
            desc: String | None = None,
            actions: dict[String, Effect] | None = None,
            environ: dict[str, object] | None = None,
            durability: vec2i | None = None,
            quantity: int = 1,
            modifiers: dict[str, object] | None = None,
            triggers: dict[str, Effect] | None = None,
            stats: WandStats | None = None,
            wand_modifiers: dict[str, object] | None = None,
            wand_triggers: dict[str, Effect] | None = None):
        super().__init__(
            name,
            icon,
            desc,
            actions,
            environ,
            durability,
            quantity,
            modifiers,
            triggers)
        assert stats is not None
        self.stats = stats
        self.wand_affixes = AffixGroup.from_config(wand_modifiers, wand_triggers)
        self.children: list[Item | None] = [None] * self.stats.capacity

    def item_to_spell(self, item: Item | None) -> Spell | None:
        if item is None:
            return None
        raise NotImplementedError

    def compile(self) -> CompiledWand:
        # 1. 拷贝一份基础属性用于修改
        stats = self.stats.copy()
        # 2. 应用法杖词条
        self.wand_affixes.apply_modifiers(stats)
        # 3. 编译法术组
        compiled = CompiledWand(stats)

        affixes = AffixGroup()
        spell_indices = []
        for i in range(len(self.children)):
            item = self.children[i]
            spell = self.item_to_spell(item)
            if spell is None:
                continue

            if isinstance(spell, WandPassive):
                spell.affixes.apply_modifiers(stats)
                continue

            spell_indices.append(i)
            if isinstance(spell, SpellBoost):
                affixes.update(spell.affixes)
            elif isinstance(spell, PrimarySpell):
                primary_spell = spell.copy()
                affixes.apply_modifiers(primary_spell)
                spell_group = SpellGroup(
                    spell=primary_spell,
                    indices=spell_indices.copy(),
                )
                compiled.spell_groups.append(spell_group)
                affixes = AffixGroup()
                spell_indices = []
        return compiled
