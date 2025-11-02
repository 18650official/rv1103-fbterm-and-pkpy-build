from typing import Self


class ValueFix:
    def __init__(self):
        self.boost: int = 0                 # 固定增加
        self.boost_pct: float = 0           # 百分比增加
        self.reduction: int = 0             # 固定减少
        self.reduction_pct: float = 0       # 百分比减少

    def merge(self, other: 'ValueFix') -> None:
        self.boost += other.boost
        self.boost_pct += other.boost_pct
        self.reduction += other.reduction
        self.reduction_pct += other.reduction_pct

    def apply_dec(self, value: int) -> int:
        value = round(value * (1 - self.reduction_pct))
        value = value - self.reduction
        return value
    
    def apply_inc(self, value: int) -> int:
        value = round(value * (1 + self.boost_pct))
        value = value + self.boost
        return value
    

class Enum[T]:
    _MAPPING: dict[T, Self] = {}

    def __init__(self, key: T):
        self.key = key
        m = type(self)._MAPPING
        assert key not in m, f'Duplicate enum key: {key}'
        m[key] = self

    @classmethod
    def from_key(cls, key: T) -> Self:
        return cls._MAPPING[key]
    
    def __reduce__(self):
        return (type(self).from_key, (self.key,))
