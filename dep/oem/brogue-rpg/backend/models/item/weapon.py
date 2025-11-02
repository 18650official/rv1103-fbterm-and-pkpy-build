from vmath import vec2i
from array2d import array2d

from backend.utils import FacingTransform
from backend.models.effect import Effect
from .base import EquippableItem


def pattern_to_offsets(pattern: str):
    lines = [
        list(line.strip())
        for line in pattern.split('\n')
        if line.strip()
    ]
    offsets: list[vec2i] = []
    a = array2d[str].fromlist(lines)
    center = a.index('P')
    for pos, val in a:
        if val == '#':
            offsets.append(pos - center)
    offsets.sort(key=lambda v: v.dot(v))
    return offsets


class Weapon(EquippableItem):
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
            min_dmg = 0,
            max_dmg = 0,
            pattern: str = """
                            ....
                            P#..
                            ....
                            """):
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
        self.min_dmg = min_dmg
        self.max_dmg = max_dmg
        self.pattern = pattern
        self.offsets = pattern_to_offsets(self.pattern)

    def player_get_auto_target(self) -> vec2i | None:
        game = current_game()
        valid_targets = self.get_valid_targets(game.hero)
        actors = game.world.actors
        for target in valid_targets:
            a = actors.get(target)
            if a is not None and a.is_mob:
                return target
        if len(valid_targets) == 0:
            return None
        return valid_targets[0]
    
    def get_valid_targets(self, src):
        targets: list[vec2i] = []
        facing = src.facing
        if facing == vec2i.ZERO:
            return targets
        trans = FacingTransform(vec2i.RIGHT, facing)
        for offset in self.offsets:
            dst_pos = src.pos + trans(offset)
            targets.append(dst_pos)
        return targets
    
    def attack(self, ctx, src, target):
        import random
        from backend.models import DamageInfo
        from backend.battle.damage import deal_damage

        yield  # TODO: 动画播放
        
        rand = random.Random()
        dmg = rand.randint(self.min_dmg, self.max_dmg)
        dst = current_world().actors.get(target)
        if dst is not None:
            dmg_info = DamageInfo('neutral', 'weapon', 'melee')
            deal_damage(rand, src, dst, dmg, dmg_info)
        return 1.0
