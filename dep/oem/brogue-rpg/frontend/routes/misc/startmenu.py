from typing import Any, Generator
from vmath import rgb

from backend.platform import VirtualKey
from frontend import ui

from ..base import Page

# https://patorjk.com/software/taag/#p=display&h=1&v=1&f=Calvin%20S&t=brogue%20rpg
LOGO = """
┌┐ ┬─┐┌─┐┌─┐┬ ┬┌─┐  ┬─┐┌─┐┌─┐
├┴┐├┬┘│ ││ ┬│ │├┤   ├┬┘├─┘│ ┬
└─┘┴└─└─┘└─┘└─┘└─┘  ┴└─┴  └─┘
""".strip()

class StartMenuPage(Page):
    def __init__(self):
        self.cursor = 0
        self.buttons = [
            tr('ui.startmenu.new_game'),
            tr('ui.startmenu.continue'),
            tr('ui.startmenu.settings'),
            tr('ui.startmenu.credit'),
            tr('ui.startmenu.quit'),
        ]

    def __call__(self, io):
        children = [ui.HDivider(), ui.Newline()]
        # logo
        for line in LOGO.split('\n'):
            line = rgb(0, 191, 255).ansi_fg(line)
            line = ui.textpad(line, io.config.width, 'center')
            children.append(line)
        children.append(ui.Newline())

        # subtitle
        children.append(ui.richtext(
                'Explore the Fantasy World of RPG2',
                width=io.config.width,
                align='center',
                fg=ui.theme.gray,
                italic=True
            )
        )
        children.append(ui.Newline())

        # buttons
        padding = io.config.width // 4
        mid_line = '─' * (io.config.width // 2)
        gray = ui.theme.gray
        buttons = []
        buttons.append(gray.ansi_fg(f'┌{mid_line}┐'))
        for i, button in enumerate(self.buttons):
            buttons.append(ui.Row([
                gray.ansi_fg('│'),
                ui.richtext(
                    f' {i+1}. {button} ',
                    bg=ui.theme.selected_bg if i == self.cursor else None,
                    width=len(mid_line)
                ),
                gray.ansi_fg('│'),
            ]))
        buttons.append(gray.ansi_fg(f'└{mid_line}┘'))

        children.append(
            ui.Padding(
                ui.Column(buttons),
                left_pad=padding,
                height=len(self.buttons) + 2,
            )
        )

        children.append(ui.Newline())
        children.append(ui.HDivider())
        return ui.Column(children, io.config.width)

    def poll(self, io) -> Generator[None, Any, int]:
        while True:
            state, axis = yield from io.input.wait_for_input()
            if axis.y != 0:
                self.move_cursor(axis.y)
            elif state[VirtualKey.OK]:
                if self.cursor == 0:
                    return 0
                elif self.cursor == 1:
                    pass
                elif self.cursor == 2:
                    pass
                elif self.cursor == 3:
                    pass
                elif self.cursor == 4:
                    pass
                else:
                    pass
            yield

    def move_cursor(self, delta: int):
        self.cursor = (self.cursor + delta) % len(self.buttons)
