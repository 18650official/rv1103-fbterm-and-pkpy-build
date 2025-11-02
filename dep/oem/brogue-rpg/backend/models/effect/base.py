from typing import TypedDict, NotRequired

class Effect:
    desc: String | None = None

    def render_desc(self, context: dict) -> str:
        raise NotImplementedError
    
    def __call__(self, context: dict):
        raise NotImplementedError
    
    @staticmethod
    def from_config(effects: 'list[str | Effect] | None' = None, desc: String | None = None) -> 'Effect':
        if effects is None:
            effects = []
        return EffectSequence(effects, desc)

class EffectSequence(Effect):
    def __init__(self, effects: list[str | Effect], desc: String | None):
        self.effects = [
            e if isinstance(e, Effect) else ScriptEffect(e)
            for e in effects
        ]
        self.desc = desc

    def __call__(self, context: dict):
        for effect in self.effects:
            effect(context)

class ScriptEffect(Effect):
    def __init__(self, source: str):
        self.code = compile(source, '<script>', 'exec')

    def __call__(self, context: dict):
        exec(self.code, context)
