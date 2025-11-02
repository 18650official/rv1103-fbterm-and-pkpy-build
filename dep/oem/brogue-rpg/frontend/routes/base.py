from typing import Any, Generator, TYPE_CHECKING

from .. import ui

if TYPE_CHECKING:
    from frontend.io import ConsoleIO


class Page[T]:
    def common_header(self, io: ConsoleIO) -> ui.Widget:
        hero = current_game().hero
        return ui.Column([
            ui.Row([
                ui.StatBarSpan('HP', io.config.bar_width, ui.theme.hp_bar_fg, hero.hp_vec2i),
                f' ({hero.shield})' if hero.shield > 0 else None,
            ]),
            ui.Row([
                ui.StatBarSpan('SP', io.config.bar_width, ui.theme.sp_bar_fg, hero.sp_vec2i),
            ]),
        ], height=2)
    
    def common_footer(self, io: ConsoleIO) -> ui.Widget:
        game = current_game()
        height = io.config.max_messages
        children = []
        for i in range(min(height, len(game.messages))):
            text = ui.richtext(
                '> ' + game.messages[i],
                fg=ui.theme.gray if i != 0 else None,
            )
            children.append(text)
        return ui.Column(children, height=height)

    def __call__(self, io: ConsoleIO) -> ui.Widget:
        raise NotImplementedError

    def poll(self, io: ConsoleIO) -> Generator[None, Any, T | None]:
        raise NotImplementedError
