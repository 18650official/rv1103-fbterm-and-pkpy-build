from backend.platform import VirtualKey, Input
from frontend import ui
from frontend.routes.base import Page

class TabController:
    pages: tuple[Page, ...]
    page_index: int | None

    def initialize(self, *pages: Page):
        self.pages = pages
        self.page_index = 0

    @property
    def current_page(self):
        assert self.page_index is not None
        return self.pages[self.page_index]

    def go_forward(self, offset: int):
        assert self.page_index is not None
        self.page_index = (self.page_index + offset) % len(self.pages)

    def test(self, state: list[bool]):
        if state[VirtualKey.F1]:
            self.go_forward(-1)
            return True
        elif state[VirtualKey.F2]:
            self.go_forward(1)
            return True
        elif state[VirtualKey.F3]:
            self.page_index = None
            return True
        return False
    

def tab_title(text: str, input: Input):
    prev = input.vkey_name(VirtualKey.F1)
    next = input.vkey_name(VirtualKey.F2)
    return ui.Row([
        f'◀ {prev}',
        ...,
        text,
        ...,
        f'{next} ▶',
    ], fg=ui.theme.title_fg, bg=ui.theme.title_bg)