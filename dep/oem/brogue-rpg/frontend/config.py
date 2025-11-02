from vmath import vec2i

class Config:
    def __init__(self):
        self.body_extent = vec2i(9, 6)
        self.body_size = self.body_extent * 2 + vec2i.ONE
        self.body_width = self.body_size.x
        self.body_height = self.body_size.y
        self.body_height_ex = self.body_height + 3

        self.bar_width = 20
        self.max_messages = 3
        self.startmenu_height = 17

        self.width = self.body_width * 2
        self.height = 23
