from .affix import AffixGroup

class Buff:
    def __init__(self, duration: float):
        self.affixes = AffixGroup()
        self.duration = duration
