from typing import Literal, TYPE_CHECKING
from random import Random
from vmath import vec2i

if TYPE_CHECKING:
    from backend.models.event import DealDamageEventParams

from backend.models import Actor, DamageType, DamageSource, DamageMethod, ValueFix, DamageInfo


DamageOutcome = Literal['miss', 'block', 'hit', 'death_hit']


def damage_total_fix(dmg_info: DamageInfo, actor: 'Actor'):
    fix = ValueFix()
    fix.merge(actor.base_stats.dmg_types[dmg_info.type])
    fix.merge(actor.base_stats.dmg_sources[dmg_info.source])
    fix.merge(actor.base_stats.dmg_methods[dmg_info.method])
    return fix


def deal_damage(
        rand: Random,
        src: 'Actor',
        dst: 'Actor',
        dmg: int,
        dmg_info: DamageInfo,
        src_pos: vec2i | None = None,
        base_hit: int = 0) -> tuple[DamageOutcome, int]:
    game = current_game()
    outcome, dmg = deal_damage_impl(rand, src, dst, dmg, dmg_info, src_pos, base_hit)
    match outcome:
        case 'miss':
            game.log(f'{src.char}攻击{dst.char}失败，未命中！')
        case 'block':
            game.log(f'{src.char}攻击{dst.char}被格挡！')
        case 'hit':
            game.log(f'{src.char}攻击{dst.char}，造成{dmg}点伤害！')
        case 'death_hit':
            game.log(f'{src.char}攻击{dst.char}，造成{dmg}点伤害，击杀了对方！')
        case _:
            assert False, outcome
    return outcome, dmg

def deal_damage_impl(
        rand: Random,
        src: 'Actor',
        dst: 'Actor',
        dmg: int,
        dmg_info: DamageInfo,
        src_pos: vec2i | None = None,
        base_hit: int = 0) -> tuple[DamageOutcome, int]:
    game = current_game()
    if dmg_info.source != 'debuff':
        # 命中判定
        src_hit = src.stats.Hit + base_hit
        dst_dodge = dst.stats.Dodge

        if dmg_info.method == 'projectile':
            # 远程攻击距离太近降低命中
            delta = (dst.pos - (src_pos or src.pos))
            distance = max(abs(delta.x), abs(delta.y))
            if distance == 2:
                src_hit -= 1
            elif distance == 1:
                src_hit -= 2

        hit_roll = rand.randint(1, 20)  # 1d20
        if hit_roll == 1:
            return 'miss', 0
        if hit_roll != 20 and hit_roll + src_hit <= dst_dodge:
            return 'miss', 0
        
        # 格挡判定（近战和投射物攻击）
        if dmg_info.method == 'melee' or dmg_info.method == 'projectile':
            if dst.stats.Block > rand.randint(0, 100):
                return 'block', 0
            
    # 计算攻方伤害加成
    dmg = max(0, damage_total_fix(dmg_info, src).apply_inc(dmg))
    # 计算守方伤害减免
    dmg = max(0, damage_total_fix(dmg_info, dst).apply_dec(dmg))

    dst.add_hp(-dmg)
    event_params: DealDamageEventParams = {
        'src': src,
        'dst': dst,
        'dmg': dmg,
        'dmg_info': dmg_info,
    }

    if dst.hp > 0:
        game.events.send(dst, 'on_post_hit', event_params)
        return 'hit', dmg
    else:
        game.world.destroy_actor(dst)
        game.events.send(dst, 'on_death_hit', event_params)
        return 'death_hit', dmg
