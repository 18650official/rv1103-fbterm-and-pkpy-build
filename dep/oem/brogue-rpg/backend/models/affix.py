from .expr import Expr
from .effect import Effect

class StopEventPropagation(Exception):
    pass

class Trigger:
    def __init__(self, event: str, priority: int, effect: Effect):
        self.event = event
        self.priority = priority
        self.effect = effect

    def __call__(self, context: dict):
        self.effect(context)
    
    def render_desc(self, context: dict) -> str:
        raise NotImplementedError


class Modifier:
    def __init__(self, src: str, v):
        self.src = src
        self.v = v

    def render_desc(self, context: dict) -> str:
        raise NotImplementedError

    def apply(self, obj, context: dict):
        v = self.v
        if isinstance(v, Expr):
            v = v(context)
        exec(f'obj.{self.src}=val', {'obj': obj, 'val': v})


class AffixGroup:
    def __init__(self):
        self.modifiers: list[Modifier] = []
        self.triggers: list[Trigger] = []

    @staticmethod
    def from_config(modifiers: dict[str, object] | None, triggers: dict[str, Effect] | None) -> 'AffixGroup':
        ag = AffixGroup()
        if modifiers is not None:
            for k, v in modifiers.items():
                ag.modifiers.append(Modifier(k, v))
        if triggers is not None:
            for k, v in triggers.items():
                ppos = k.find(':')
                if ppos != -1:
                    event, priority = k[:ppos], int(k[ppos+1:])
                else:
                    event, priority = k[:], 0
                assert isinstance(v, Effect)
                trigger = Trigger(event, priority, v)
                ag.triggers.append(trigger)
        return ag

    def render_desc(self, context: dict) -> list[str]:
        lines = []
        for mod in self.modifiers:
            lines.append(mod.render_desc(context))
        for trg in self.triggers:
            lines.append(trg.render_desc(context))
        return lines

    def update(self, other: 'AffixGroup'):
        self.modifiers.extend(other.modifiers)
        self.triggers.extend(other.triggers)

    def copy(self):
        ag = AffixGroup()
        ag.update(self)
        return ag
    
    def apply_modifiers(self, obj, ctx: dict | None = None) -> None:
        if ctx is None:
            ctx = {}
        for mod in self.modifiers:
            mod.apply(obj, ctx)

    def __bool__(self) -> bool:
        return bool(self.modifiers) or bool(self.triggers)
