from typing import TYPE_CHECKING, Iterable
import json

from .models.actor import Hero, TurnBasedActor
from .models.event import EventDispatcher
from .i18n import String

if TYPE_CHECKING:
    from .world import World
    from .io import IO

from .platform import load_asset

class Locale:
    def __init__(self, src_code: str):
        self.src = self.load(src_code)
        self.dst = {}

    def load(self, code: str):
        s = load_asset(f'assets/locale/{code}.json')
        return json.loads(s)
        
    def switch(self, code: str):
        self.dst = self.load(code)

    def gettext(self, key: str) -> str:
        return self.dst.get(key, self.src.get(key, key))


class Game:
    instance: 'Game'

    def __init__(self, io: IO, world: World, hero: Hero) -> None:
        Game.instance = self
        self.io = io
        self.locale = Locale('zh-CN')
        self.world = world
        self.hero = hero
        self.messages: list[str] = []
        self.events = EventDispatcher()

    def log(self, msg: str):
        self.messages.insert(0, msg)
        if len(self.messages) > 10:
            self.messages.pop()

    def __iter__(self):
        yield from self.io.wait_for_game_start()

        while True:
            tb_actors: Iterable[TurnBasedActor] = self.world.actors.values()
            # determine the next actor to act
            # 1. the actor with the smallest time acts first
            # 2. if multiple actors have the same time, the actor with the highest priority acts first
            actor = min(tb_actors, key=lambda u: (u.tb_info.time, -u.tb_info.priority))
            context = {}
            duration = yield from actor.act(context)
            assert isinstance(duration, float)
            assert duration >= 0.0
            actor.tb_info.time += duration


# inject to builtins
import builtins

setattr(builtins, 'current_game', lambda: Game.instance)
setattr(builtins, 'current_world', lambda: Game.instance.world)
setattr(builtins, 'current_io', lambda: Game.instance.io)
setattr(builtins, 'tr', lambda key: String(key))
setattr(builtins, 'formula', lambda x: x)
