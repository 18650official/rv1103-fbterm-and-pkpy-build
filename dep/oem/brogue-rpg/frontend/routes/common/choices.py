from typing import Any, Generator

from backend.platform import VirtualKey
from frontend import ui

from ..base import Page


class Option:
    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled


class ChoicesPage(Page[int]):
    def __init__(self, options: list[Option], title: str, desc: str, cursor: int = 0):
        self.options = [o for o in options if o.enabled]
        self.title = title
        self.desc = desc
        self.cursor = cursor

    def poll(self, io) -> Generator[None, Any, int]:
        while True:
            state, axis = yield from io.input.wait_for_input()
            self.cursor = (self.cursor + axis.y) % len(self.options)
            if state[VirtualKey.OK]:
                return self.cursor
            elif state[VirtualKey.F3]:
                return -1
            yield

    def __call__(self, io):
        desc_height = 7
        choice_height = io.config.body_height_ex - desc_height - 2

        body = ui.Column([
            ui.richtext(
                f' {i + 1}. {option.name}',
                width=io.config.width,
                bg=ui.theme.selected_bg if i == self.cursor else None,
            )
            for i, option in enumerate(self.options)
            ],
            height=choice_height,
        )
        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            ui.Row([
                ...,
                self.title,
                ...,
            ], fg=ui.theme.title_fg, bg=ui.theme.title_bg),
            body,
            ui.HDivider(),
            ui.MultiLineText(
                self.desc,
                width=io.config.width,
                height=desc_height,
            ),
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)
    
