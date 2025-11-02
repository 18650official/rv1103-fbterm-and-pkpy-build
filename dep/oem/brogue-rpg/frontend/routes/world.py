from typing import TYPE_CHECKING
from vmath import vec2i, color32
from array2d import array2d
from backend import World

from frontend import ui
from .base import Page

if TYPE_CHECKING:
    from frontend import ConsoleIO
    from backend.models.actor import Actor


class Cursor:
    actor: 'Actor | None'

    def __init__(self):
        self.actor = None
        self._offset = vec2i.ZERO
        self.enabled = False

    def reset(self):
        self.actor = None
        self._offset = vec2i.ZERO
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled
        if not self.enabled:
            self.reset()
        return self.enabled
    
    @property
    def base_postion(self) -> vec2i:
        if self.actor:
            return self.actor.pos
        else:
            return current_game().hero.pos

    @property
    def position(self) -> vec2i:
        return self._offset + self.base_postion
    
    @position.setter
    def position(self, pos: vec2i):
        self.actor = None
        base = current_game().hero.pos
        self._offset = pos - base

    def get_actor(self, must_locked=False):
        if self.actor is not None:
            return self.actor
        if must_locked:
            return None
        return current_world().actors.get(self.position)


class WorldPage(Page):
    def __init__(self):
        self.cursor = Cursor()
        self.charge_value = 0.0

        self.facing_icon = {
            vec2i.UP: '↑',
            vec2i.DOWN: '↓',
            vec2i.LEFT: '←',
            vec2i.RIGHT: '→',
            vec2i.ZERO: '-',
        }

    def render_world(self, io: ConsoleIO):
        game = current_game()
        width, height = io.config.body_size
        zone = game.world.tiles.view_rect(
            game.hero.pos - io.config.body_extent,
            width,
            height
        )

        m = array2d[str](zone.width, zone.height, default='　')
        m_bg = array2d[color32 | None](zone.width, zone.height, default=None)

        from backend.world.schema.tile import Tile

        # 绘制地形
        for layer in ['t_ground', 't_floor', 't_plant', 't_block']:
            for pos, tile_stack in zone:
                t: Tile | None = getattr(tile_stack, layer)
                if t is None:
                    continue
                # 背景色混合
                if t.bg is not None:
                    m_bg[pos] = color32.alpha_blend(t.bg, m_bg[pos])
                # 前景色覆盖
                if t.fg is not None:
                    m[pos] = t.fg.ansi_fg(t.char)
                else:
                    m[pos] = t.char

        # 绘制光标
        cursor_pos = self.cursor.position - zone.origin
        m_bg[cursor_pos] = color32.alpha_blend(
            ui.theme.cursor_bg,
            m_bg[cursor_pos]
        )

        # 绘制单位
        for pos, actor in game.world.actors.items():
            pos -= zone.origin
            if zone.is_valid(pos):
                m[pos] = actor.char

        # 应用颜色
        for pos, tile in zone:
            fg, bg = m[pos], m_bg[pos]
            if bg is not None:
                m[pos] = bg.ansi_bg(fg)
        
        return m.render()
    
    def render_status(self, io: ConsoleIO):
        # progress bar
        hero = current_game().hero
        children = []
        icon = self.facing_icon[hero.facing]
        children.append(f"边境小镇: {hero.pos.x}, {hero.pos.y} ({icon})")
        # 检测光标位置的物体
        actor = self.cursor.get_actor()
        if actor is None:
            children.append("-> 没有对象")
        else:
            if actor.is_hero:
                children.append("-> 你自己")
            else:
                children.append(f"-> {actor.char} HP: {actor.hp_vec2i}")

        # total_seconds = 0.7
        # current_game().message(str(current_io().delta_time))
        # self.charge_value += current_io().delta_time / total_seconds

        # children[0] = ui.Row(
        #     [
        #         ui.ChargeBarSpan(self.charge_value, 2, width=renderer.width)
        #     ],
        # )
        return ui.Column(children, io.config.width, height=2)

    def __call__(self, io):
        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            ui.Image(self.render_world(io)),
            ui.HDivider(),
            self.render_status(io),
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)