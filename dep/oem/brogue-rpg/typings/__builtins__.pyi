from backend import Game, World, IO, i18n
from typing import Generator, TypeVar
import builtins

# injected functions
def current_game() -> Game: ...
def current_world() -> World: ...
def current_io() -> IO: ...

# type aliases
String = i18n.String
ellipsis = builtins.ellipsis

_T = TypeVar('_T')
Future = Generator[None, None, _T]

# i18n
def tr(key: str) -> i18n.String: ...

# preview formula for VSCode
def formula[T](x: T) -> T: ...
