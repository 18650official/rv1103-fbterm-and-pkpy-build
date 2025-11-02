from typing import Sequence
from ..base import Widget

class _Stack(Widget):
    children: list[Widget]

    def __init__(self, children: Sequence[Widget | None], width=-2, height=-2):
        super().__init__(width, height)
        self.children = [child for child in children if child is not None]

    def __getitem__(self, index: int):
        return self.children[index]
    
    def __len__(self):
        return len(self.children)


class HStack(_Stack):
    def prerender(self, width, height):
        super().prerender(width, height)
        assert self.height > 0
        total_width = 0
        for child in self.children:
            assert child.width >= 0
            total_width += child.width
            child.prerender(child.width, self.height)
            assert child.height == self.height
        if self.width < 0:
            self.width = total_width
        else:
            assert (self.width == total_width), f"{self.width} != {total_width}"

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        output = [child.render() for child in self.children]
        lines = []
        for i in range(self.height):
            line = ''.join([child[i] for child in output])
            lines.append(line)
        return lines
    
class VStack(_Stack):
    def prerender(self, width, height):
        super().prerender(width, height)
        assert self.width > 0
        total_height = 0
        for child in self.children:
            assert child.height >= 0
            total_height += child.height
            child.prerender(self.width, child.height)
            assert child.width == self.width
        if self.height < 0:
            self.height = total_height
        else:
            assert (self.height == total_height), f"{self.height} != {total_height}"

    def render(self) -> list[str]:
        assert self.width > 0 and self.height > 0
        lines = []
        for child in self.children:
            lines.extend(child.render())
        assert len(lines) == self.height, f'{len(lines)} != {self.height}'
        return lines
