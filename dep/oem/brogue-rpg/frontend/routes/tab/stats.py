from frontend.routes.base import Page
from frontend import ui

from vmath import rgb

from .base import TabController, tab_title

class StatsPage(Page):
    def __init__(self, controller: TabController):
        self.controller = controller

    def poll(self, io):
        while True:
            state, axis = yield from io.input.wait_for_input()
            if self.controller.test(state):
                break

    def stat_alloc(self, name, current):
        return ui.Row([
            ui.TextSpan(f' {name}: {current}'),
            ...,
            ui.TextSpan('( + )'),
        ])

    def __call__(self, io):
        half_width = io.config.width // 2 - 1
        half_width2 = io.config.width - half_width - 1
        upper_height = 9

        hero = current_game().hero

        body = ui.Column(
            [
                tab_title("属性界面", io.input),
                ui.Text(f' 等级: {hero.level}'),
                ui.Text(f' 经验: {hero.exp} / {hero.next_level_exp()}'),
                ui.HDivider(),
                ui.HStack([
                    ui.Column([
                        self.stat_alloc("体质", hero.stats.Vit),
                        self.stat_alloc("力量", hero.stats.Str),
                        self.stat_alloc("智力", hero.stats.Int),
                        self.stat_alloc("精神", hero.stats.Spi),
                        self.stat_alloc("幸运", hero.stats.Luk),
                        ui.Row([
                            ...,
                            ui.TextSpan(f'未分配点数: {hero.stats.Unused}'),
                            ...,
                        ], bg=rgb(50, 50, 50)),
                        ], width=half_width),
                    ui.VDivider(fillchar=' | '),
                    ui.Column([
                        ui.Text(f'HP: {hero.hp} / {hero.stats.MaxHP}'),
                        ui.Text(f'SP: {hero.sp} / {hero.stats.MaxSP}'),
                        ui.Newline(),
                        ui.Text(f'Dodge: {hero.stats.Dodge}'),
                        ui.Text(f'Block: {hero.stats.Block}'),
                        ui.Newline(),
                        ui.Text(f'Armor: {hero.stats.Armor}'),
                        ui.Text(f'Res: {hero.stats.ansi_colored_resist()}'),
                    ], width=half_width2),
                ], height=-1),
            ],
            height=io.config.body_height_ex
        )

        return ui.VStack([
            self.common_header(io),
            ui.HDivider(),
            body,
            ui.HDivider(),
            self.common_footer(io),
        ], width=io.config.width)