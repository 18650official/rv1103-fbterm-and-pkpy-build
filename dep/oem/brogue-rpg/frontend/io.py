from typing import Any, Generator
from vmath import vec2i

from backend import IO
from backend.platform import VirtualKey, Input, clear_screen

from frontend import routes

from .config import Config


class ConsoleIO(IO):
    pages: list[routes.Page]

    def __init__(self) -> None:
        super().__init__()
        self.input = Input()

        self.pages = []
        self.config = Config()

        self.page_startmenu = routes.misc.StartMenuPage()
        self.page_world = routes.world.WorldPage()
        self.page_tab = routes.tab.TabPage()

        # cache
        self.cursor = self.page_world.cursor

    def push[T](self, page: 'routes.Page[T]'):
        self.pages.append(page)
        res = yield from page.poll(self)
        self.pages.pop()
        return res
    
    def begin_frame(self):
        super().begin_frame()

    def end_frame(self):
        super().end_frame()
        w = self.pages[-1](self)
        w.prerender(self.config.width, self.config.height)
        assert w.width == self.config.width
        assert w.height == self.config.height
        clear_screen()
        print(*w.render(), sep='\n', flush=True)
        # update the input state
        self.input.update()

    def wait_for_input_and_act(self, context: dict) -> Future[float]:
        game = current_game()
        while True:
            state, axis = yield from self.input.wait_for_input()

            if state[VirtualKey.TAB]:
                if self.cursor.enabled:
                    game.log("光标模式下无法打开背包")
                    # TODO: 特殊处理
                    continue
                game.log("打开背包")
                cmd = yield from self.push(self.page_tab.with_index(0))
                if cmd is not None:
                    return cmd
                continue
            ###############################################

            # if state[VirtualKey.IDLE]:
            #     return 1.0

            # if state[VirtualKey.CURSOR_MODE]:
            #     if self.cursor.toggle():
            #         game.log("开启光标模式")
            #     else:
            #         game.log("关闭光标模式")
            #     continue

            ###############################################

            if state[VirtualKey.OK]:
                target = game.hero.pos + game.hero.facing
                # cmd = game.world.interact(game.hero, target)
                cmd = None
                if cmd is not None:
                    return cmd
                else:
                    weapon = game.hero.equipments.weapon.item
                    if weapon is None:
                        game.log("未装备武器，无法攻击")
                        continue
                    target = weapon.player_get_auto_target()
                    if target is None:
                        game.log("没有目标，无法攻击")
                        continue
                    self.cursor.position = target
                    # do attack
                    res = yield from weapon.attack(context, game.hero, target)
                    return res
 
            if axis != vec2i.ZERO:
                if self.cursor.enabled:
                    self.cursor.position += axis
                else:
                    self.cursor.reset()
                    target = game.hero.pos + axis
                    game.hero.face_direction(axis)
                    if game.world.is_walkable(target):
                        current_world().move_actor(game.hero, axis)
                        game.events.broadcast('on_hero_move', None)
                        return 1.0
                    else:
                        game.log("这里有障碍物，无法前进")
                        return 1.0

    def wait_for_game_start(self):
        yield from self.push(self.page_startmenu)
        self.pages.append(self.page_world)

    def choices(
            self,
            options: list[routes.common.Option],
            title: str,
            desc: str,
            cursor: int = 0
            ) -> Generator[None, Any, int | None]:
        return self.push(routes.common.ChoicesPage(options, title, desc, cursor))

    def wait_for_confirm(self):
        yield
        while True:
            state, _ = yield from self.input.wait_for_input()
            if state[VirtualKey.OK]:
                return
            yield

    def choose_item_slot(self, filter, **kwargs):
        # inventory = current_game().hero.inventory
        # return self.renderer.push(InventoryChoicePage(inventory, filter=filter))
        raise NotImplementedError

