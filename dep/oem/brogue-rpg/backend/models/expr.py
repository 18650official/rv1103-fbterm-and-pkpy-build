class Expr:
    def __init__(self, source: str) -> None:
        self.code = compile(source, '<string>', 'eval')

    def __call__(self, context: dict):
        return eval(self.code, context)
