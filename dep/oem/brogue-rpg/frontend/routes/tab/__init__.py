from frontend.routes.base import Page

from .inventory import InventoryPage
from .equipments import EquipmentsPage
from .talents import TalentsPage
from .crafting import CraftingPage
from .pet import PetPage
from .stats import StatsPage

from .base import TabController

class TabPage(Page):
    def __init__(self):
        self.controller = TabController()
        self.controller.initialize(
            InventoryPage(self.controller),     # 0
            EquipmentsPage(self.controller),    # 1
            TalentsPage(self.controller),       # 2
            CraftingPage(self.controller),      # 3
            PetPage(self.controller),           # 4
            StatsPage(self.controller),         # 5
        )

    def with_index(self, page_index: int):
        self.controller.page_index = page_index
        return self

    def poll(self, io):
        while True:
            page = self.controller.current_page
            res = yield from page.poll(io)
            if res is not None:
                return res
            if self.controller.page_index is None:
                return None
            
    def __call__(self, io):
        page = self.controller.current_page
        return page(io)