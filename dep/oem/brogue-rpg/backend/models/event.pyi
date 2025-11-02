from typing import Literal, overload, TypedDict
from backend.battle.damage import DamageInfo
from backend.models.actor import Actor
from backend.models.affix import Trigger

Event = Literal[
    'on_hero_move',
    'on_hero_attack',
]

LocalEvent = Literal[
    'on_post_hit',
    'on_death_hit',
]

class DealDamageEventParams(TypedDict):
    src: Actor
    dst: Actor
    dmg: int
    dmg_info: DamageInfo

class EventDispatcher:
    @overload
    def broadcast(self, event: Literal['on_hero_move'], params: None): ...
    @overload
    def broadcast(self, event: Literal['on_hero_attack'], params: None): ...

    @overload
    def send(self, actor: Actor, event: Literal['on_post_hit'], params: DealDamageEventParams): ...
    @overload
    def send(self, actor: Actor, event: Literal['on_death_hit'], params: DealDamageEventParams): ...

    def add_trigger(self, trigger: Trigger) -> None: ...
