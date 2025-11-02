from typing import Optional, Literal
from vmath import color32, rgb
from unicodedata import east_asian_width


Align = Literal['left', 'right', 'center']

_WCWIDTH_MAP = {
    'F': 2,
    'H': 1,
    'W': 2,
    'Na': 1,
    'A': 1,
    'N': 1,
}

def wcwidth(c: str) -> int:
    if 32 <= ord(c) < 0x7f:
        return 1
    w = east_asian_width(c)
    return _WCWIDTH_MAP[w]

def ansi_italic(text: str):
    return f'\x1b[3m{text}\x1b[0m'


class Char:
    def __init__(self, c: str, fg: Optional[color32], bg: Optional[color32], italic: bool):
        self.c = c
        self.fg = fg
        self.bg = bg
        self.italic = italic
        self.width = wcwidth(c)

    def ansi_prefix(self) -> str:
        buf = []
        fg, bg, italic = self.fg, self.bg, self.italic
        if fg is not None:
            buf.append(f'\x1b[38;2;{fg.r};{fg.g};{fg.b}m')
        if bg is not None:
            buf.append(f'\x1b[48;2;{bg.r};{bg.g};{bg.b}m')
        if italic:
            buf.append('\x1b[3m')
        return ''.join(buf)

    def render(self):
        prefix = self.ansi_prefix()
        if prefix:
            return f'{prefix}{self.c}\x1b[0m'
        return self.c
    
    def __repr__(self):
        return f"Char({self.c!r}, fg={self.fg!r}, bg={self.bg!r}, italic={self.italic!r}, width={self.width!r})"

SPACE = Char(' ', None, None, False)

class Line:
    chars: list[Char]

    def __init__(self):
        self.chars = []

    def __getitem__(self, index: int):
        return self.chars[index]

    def __len__(self):
        return len(self.chars)

    def append(self, c: Char):
        self.chars.append(c)
    
    def copy(self):
        line = Line()
        line.chars.extend(self.chars)
        return line

    def render(self) -> str:
        # return ''.join([c.render() for c in self.chars])
        prefix = ''
        buf = []
        for c in self.chars:
            new_prefix = c.ansi_prefix()
            if new_prefix != prefix:
                if prefix:
                    buf.append('\x1b[0m')
                prefix = new_prefix
                buf.append(prefix)
            buf.append(c.c)
        if prefix:
            buf.append('\x1b[0m')
        return ''.join(buf)
    
    def total_width(self) -> int:
        total = 0
        for c in self.chars:
            total += c.width
        return total
    
    def clip(self, width: int):
        total = 0
        line = Line()
        for c in self.chars:
            if total + c.width >= width:
                break
            line.append(c)
            total += c.width
        assert total == line.total_width()
        if total < width:
            line.chars.extend([SPACE] * (width - total))
        return line
    
    def pad(self, width: int, align: Align, clip: bool):
        line = self.copy()
        total = line.total_width()
        if total >= width:
            if clip and total > width:
                line = line.clip(width)
            return line
        if align == 'left':
            line.chars.extend([SPACE] * (width - total))
            return line
        if align == 'right':
            line.chars = [SPACE] * (width - total) + line.chars
            return line
        if align == 'center':
            left = (width - total) // 2
            right = width - total - left
            line.chars = [SPACE] * left + line.chars + [SPACE] * right
            return line
        assert False

    def wrap(self, width: int):
        lines: list[Line] = []
        buf = Line()
        buf_width = 0
        for c in self.chars:
            buf_width += c.width
            if buf_width > width:
                lines.append(buf)
                buf = Line()
                buf_width = c.width
            buf.append(c)
        if buf:
            lines.append(buf)
        return lines

    @staticmethod
    def parse(text: str):
        fg: Optional[color32] = None
        bg: Optional[color32] = None
        italic = False
        chars: list[str] = list(text)
        line = Line()
        i = 0
        while i < len(chars):
            c = chars[i]
            if c == '\x1b':
                # \x1b[38;2;%d;%d;%dm
                # \x1b[48;2;%d;%d;%dm
                # \x1b[3m
                # \x1b[0m
                j = chars.index('m', i)
                fmt = text[i: j+1]
                if fmt.startswith('\x1b[38;2;'):
                    r, g, b = [int(x) for x in fmt[7:-1].split(';')]
                    fg = rgb(r, g, b)
                elif fmt.startswith('\x1b[48;2;'):
                    r, g, b = [int(x) for x in fmt[7:-1].split(';')]
                    bg = rgb(r, g, b)
                elif fmt == '\x1b[3m':
                    italic = True
                elif fmt == '\x1b[0m':
                    fg = None
                    bg = None
                    italic = False
                else:
                    raise ValueError(f"unknown ansi code: {fmt!r}")
                i = j + 1
            else:
                assert c != '\n'
                line.append(Char(c, fg, bg, italic))
                i += 1
        return line


def textwidth(text: str) -> int:
    line = Line.parse(text)
    return line.total_width()

def textclip(text: str, width: int) -> str:
    line = Line.parse(text)
    line = line.clip(width)
    return line.render()

def textpad(text: str, width: int, align: Align = 'left', clip=True) -> str:
    line = Line.parse(text)
    line = line.pad(width, align, clip)
    assert line.total_width() == width
    return line.render()

def textwrap(text: str, width: int):
    assert width > 0
    res: list[str] = []
    for line in text.split('\n'):
        if line == '':
            res.append('')
            continue
        lines = Line.parse(line).wrap(width)
        for line in lines:
            res.append(line.render())
    return res

def textpad2d(lines: list[str], width: int, height: int, clip=True):
    res = lines.copy()
    if len(res) < height:
        res.extend([''] * (height - len(res)))
    if len(res) > height:
        if clip:
            res = res[:height]
        else:
            raise ValueError(f"too many lines: {len(res)} > {height}")
    for i in range(len(res)):
        res[i] = textpad(res[i], width, 'left', clip)
    return res


__all__ = [
    'Align',
    'ansi_italic',
    'Char',
    'Line',
    'textwidth',
    'textclip',
    'textpad',
    'textwrap',
    'textpad2d',
    'SPACE',
]