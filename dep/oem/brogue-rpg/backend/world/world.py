from vmath import vec2i
from collections import deque
import random
from typing import Iterable

from backend.models.actor import Actor
from backend.utils import DIRS_4_CW, DIRS_8_CW

from .schema.world import World as BaseWorld


class World(BaseWorld):
    def __init__(self):
        super().__init__()
        self.actors = dict[vec2i, Actor]()
        self.rand = random.Random(7)
        self.hero_last_region_id = ''

    def on_hero_enter_region(self, pos: vec2i, region_id: str) -> None:
        pass

    def spawn_actor[T: Actor](self, t: type[T], pos: vec2i) -> T:
        actor = t()
        actor.pos = pos
        # don't modify default!!! e.g. get an inexistent key (default object) and modify it
        self.actors[pos] = actor
        if actor.is_hero:
            self.hero_last_region_id = self.tiles[pos].region_id
        return actor

    def destroy_actor(self, actor: Actor) -> None:
        del self.actors[actor.pos]

    def move_actor(self, actor: Actor, delta: vec2i) -> None:
        self.teleport_actor(actor, actor.pos + delta)

    def teleport_actor(self, actor: Actor, target: vec2i) -> None:
        del self.actors[actor.pos]
        actor.pos = target
        self.actors[actor.pos] = actor
        if actor.is_hero:
            new_region_id = self.tiles[target].region_id
            if new_region_id != self.hero_last_region_id:
                self.hero_last_region_id = new_region_id
                self.on_hero_enter_region(target, new_region_id)

    # def interact(self, actor: Actor, target: vec2i) -> Task | None:
    #     """让actor和target位置的单位进行交互，如果可行的话，返回一个命令"""
    #     for pos, fg in self.actors.items():
    #         if pos == target:
    #             return fg.interact(actor)

    def is_walkable(self, pos: vec2i) -> bool:
        """检查坐标是否是可行走的"""
        return self.tiles[pos].is_walkable() and pos not in self.actors

    def bfs(self, pos: vec2i, filter=None) -> Iterable[tuple[vec2i, int]]:
        """由近及远地搜索满足条件的坐标，迭代地返回一个包含坐标和距离的元组"""
        filter = filter or self.is_walkable
        q = deque[tuple[vec2i, int]]()
        visited = set[vec2i]()
        q.appendleft((pos, 0))
        visited.add(pos)
        while len(q) > 0:
            pos, dist = q.pop()
            yield pos, dist
            for delta in DIRS_4_CW:
                next_pos = pos + delta
                if next_pos in visited:
                    continue
                if not filter(next_pos):
                    continue
                q.appendleft((next_pos, dist+1))
                visited.add(next_pos)
