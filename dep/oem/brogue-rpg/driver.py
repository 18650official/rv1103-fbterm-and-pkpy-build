import backend
from frontend import ConsoleIO

world, hero = backend.levels.Playground.build_world()

# 创建游戏
io = ConsoleIO()
game = backend.Game(io, world, hero)
game_iterator = iter(game)

import pkpy
pkpy.enable_full_buffering_mode()

print('\x1bc', flush=True)

def step_game():
    """Step the game and render the result.
    
    Return `False` if the game is over, otherwise `True`.
    """
    io.begin_frame()
    res = next(game_iterator, StopIteration)
    io.end_frame()
    return res is not StopIteration
