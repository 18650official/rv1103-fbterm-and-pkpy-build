from typing import Generator
import pkpy
import time
import sys

class IO:
    def __init__(self):
        self.delta_time = 0.0
        self.time = 0.0
        self.is_first_frame = True
        self.is_desktop = sys.platform in ['win32', 'darwin', 'linux']

    def begin_frame(self) -> None:
        if self.is_desktop:
            pkpy.watchdog_begin(1000)
        now = time.time()
        if self.is_first_frame:
            self.delta_time = 0.0
            self.is_first_frame = False
        else:
            self.delta_time = now - self.time
        self.time = now

    def end_frame(self) -> None:
        if self.is_desktop:
            pkpy.watchdog_end()

    def wait_for_input_and_act(self, context: dict) -> Future[float]:
        """获取玩家输入并行动"""
        raise NotImplementedError
    
    def wait_for_game_start(self) -> Generator:
        """等待游戏开始"""
        raise NotImplementedError