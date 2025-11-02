from array2d import *
from vmath import *

from typing import Literal
import random

from backend.platform import clear_screen
from frontend.renderer import ansi_bg, ansi_fg

# 基于读档的回溯通用型更强，可以存储多个解，而普通回溯只能维持一个解
# 每次迭代，注册的agent每人行动一次（单个agent不能单独回档了）

class AreaContext:
    pass

WorldType = chunked_array2d[int, None]

class Dice:
    def __init__(self, rand: random.Random, initial_counter: int):
        self.rand = rand
        self.counter = initial_counter

    @property
    def prob(self):
        threshold = 3
        if self.counter <= threshold:
            return 0
        return (self.counter - threshold) * 5
    
    def copy(self):
        return Dice(self.rand, self.counter)

    def __call__(self):
        ok = self.rand.randint(1, 100) <= self.prob
        if ok:
            self.counter = 0
        else:
            self.counter += 1
        return ok
    
class Const:
    Void = 0
    Path = 1
    Room = 2
    Protect = 8

AgentStepResult = Literal['move', 'place_room', 'dead_end']

class Agent:
    def __init__(self):
        self.rand = random.Random()
        self.pos = vec2i(0, 0)
        self.direction = self.rand.choice([vec2i.UP, vec2i.RIGHT, vec2i.DOWN, vec2i.LEFT])
        self.dice_change_direction = Dice(self.rand, 0)
        self.dice_place_room = Dice(self.rand, 100)
    
    def copy(self):
        new_agent = Agent()
        new_agent.rand = self.rand
        new_agent.pos = self.pos
        new_agent.direction = self.direction
        new_agent.dice_change_direction = self.dice_change_direction.copy()
        new_agent.dice_place_room = self.dice_place_room.copy()
        return new_agent
    
    def step(self, world: WorldType) -> AgentStepResult:
        print(f'step(): prob_change_direction: {agent.dice_change_direction.prob}%, prob_place_room: {agent.dice_place_room.prob}%')

        if self.dice_place_room():
            if self.place_room(world):
                return 'place_room'
            # cannot place room, fallback to move

        ok, is_dir_changed = self.move(world)
        if not ok:
            return 'dead_end'
        return 'move'
    
    def set_curr_pos_as_path(self, world: WorldType, pos: vec2i):
        assert world[pos] in (Const.Void, Const.Protect)
        world[pos] = Const.Path
        self.pos = pos

    def get_possible_3dirs(self) -> list[vec2i]:
        dirs = [vec2i.UP, vec2i.RIGHT, vec2i.DOWN, vec2i.LEFT]
        dirs.remove(self.direction * -1)
        self.rand.shuffle(dirs)
        return dirs

    def place_room(self, world: WorldType) -> bool:
        width = self.rand.randint(3, 9)
        height = self.rand.randint(3, 6)

        if self.direction.x == 0:   # vertical
            main_axis_length = height
            cross_axis_length = width
        else:                       # horizontal
            main_axis_length = width
            cross_axis_length = height

        """
                   ################### --
                   #                 # |
                   #                 # |
        direction  #                 # cross_axis
              --> A* center_pos      # |
                   #                 # |
                   ################### --
                   |--- main_axis ---|
        """

        center_pos = self.pos + self.direction
        dir_ccw = vec2i(self.direction.y, -self.direction.x)
        dir_cw = vec2i(-self.direction.y, self.direction.x)

        def view(extended_unit: int):
            side_pos_ccw = center_pos + dir_ccw * (cross_axis_length // 2 + extended_unit)
            side_pos_cw = center_pos + dir_cw * (cross_axis_length - cross_axis_length // 2 - 1 + extended_unit)
            side_pos_ccw_2 = side_pos_ccw + self.direction * (main_axis_length - 1 + extended_unit)
            side_pos_cw_2 = side_pos_cw + self.direction * (main_axis_length - 1 + extended_unit)
            # get left-top pos from 4 side pos

            side_pos_list = [side_pos_ccw, side_pos_cw, side_pos_ccw_2, side_pos_cw_2]
            side_pos_list.sort(key=lambda v: (v.x, v.y))
            left_top = side_pos_list[0]
            right_bottom = side_pos_list[-1]
            return world.view_rect(left_top, right_bottom.x - left_top.x + 1, right_bottom.y - left_top.y + 1) 
        
        extended_room_view = view(1)
        room_view = view(0)
        if (extended_room_view != Const.Void).any():
            return False
        
        # extended_room_view[:, :] = Const.Protect
        room_view[:, :] = Const.Room

        # goto room exit
        pos = center_pos
        found = False
        for _ in range(1000):
            pos += self.direction
            if world[pos] == Const.Void:
                # if we break here, the agent is moving out of the room
                found = True
                break
            if self.dice_change_direction():
                dirs = self.get_possible_3dirs()
                self.direction = self.rand.choice(dirs)
        assert found
        self.set_curr_pos_as_path(world, pos)
        return True

    def move(self, world: WorldType) -> tuple[bool, bool]:
        dirs = self.get_possible_3dirs()
        curr_dir_i = dirs.index(self.direction)
        if self.dice_change_direction():
            dirs[curr_dir_i], dirs[-1] = dirs[-1], dirs[curr_dir_i]
        else:
            dirs[curr_dir_i], dirs[0] = dirs[0], dirs[curr_dir_i]
        ok = False
        is_dir_changed = False
        for new_dir in dirs:
            pos = self.pos + new_dir
            pos_radius_1 = world.view_rect(pos - vec2i.ONE, 3, 3)
            if world[pos] == Const.Void and pos_radius_1.count(Const.Void) >= 7:
                ok = True
                is_dir_changed = self.direction != new_dir
                self.direction = new_dir
                self.set_curr_pos_as_path(world, pos)
                break
        return ok, is_dir_changed

def mapper(x: int):
    s = f'{x:2}'
    if x == Const.Void:
        return ansi_fg(s, vec3i.ONE * 100)
    if x == Const.Protect:
        return s
    if x == Const.Path:
        return ansi_bg(s, vec3i.ONE * 75)
    return ansi_bg(s, vec3i(0, 110, 0))

world = WorldType(4, default=0)
agent = Agent()

saved_world = None
saved_agent = None


def draw_world():
    clear_screen()
    print(f'iteration: {iteration}, pos: {agent.pos}, direction: {agent.direction}')

    world_view = world.view()
    buffer = world_view.map(mapper)
    local_agent_pos = agent.pos - world_view.origin
    buffer[local_agent_pos] = ansi_bg(' A', vec3i(150, 150, 150))
    print(buffer.render())

backup = []

iteration = 0
while True:
    backup.append((world.copy(), agent.copy()))
    
    iteration += 1
    res = agent.step(world)
    if res == 'dead_end':
        raise RuntimeError('dead end')

    draw_world()
    while input() == 'r':
        assert iteration > 1
        world, agent = backup.pop()
        iteration -= 1
        draw_world()





