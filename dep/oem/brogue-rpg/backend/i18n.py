class String:
    def __init__(self, key: str, fmt_args=None):
        self.key = key
        self.fmt_args = fmt_args

    def __hash__(self):
        return hash(self.key)
    
    def __eq__(self, other):
        if not isinstance(other, String):
            return NotImplemented
        return self.key == other.key and self.fmt_args == other.fmt_args
    
    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        text = current_game().locale.gettext(self.key)
        if self.fmt_args:
            text = text.format(*self.fmt_args)
        return text
    
    def format(self, *args):
        assert self.fmt_args is None
        return String(self.key, args)
    
    def __repr__(self):
        return f"i18n.string({self.key!r})"

    def __reduce__(self):
        return type(self), (self.key,)

