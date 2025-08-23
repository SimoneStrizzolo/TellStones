# %%
#!pip install nbimporter
#!pip install ipynb
import random, string

class StoneOld(dict):
    def __init__(self, name=None, hidden=False):
        name = name if name else ''.join(random.choices(string.ascii_letters, k=5))
        super().__init__({"_name": name, "_hidden": hidden})
    
    @property
    def name(self):
        return self['_name']

    @property
    def hidden(self):
        return self['_hidden']
    @hidden.setter
    def hidden(self, arg):
        self['_hidden'] = arg
    
    @classmethod
    def from_dict(cls, kwarg:dict):
        return cls(name=kwarg.get('name'), hidden=kwarg.get('hidden'))

    def __repr__(self):
        return "*" if self.hidden else self.name
    
    def flip(self):
        self.hidden = not self.hidden

def to_stone(arg):
    return arg if isinstance(arg, StoneOld) else StoneOld(name=arg)

# %%
from dataclasses import dataclass, field
import random, string

class StoneClassic:
    def __init__(self, name=None, hidden=False):
        self.name = name or StoneClassic._random_name()
        self.hidden = hidden

    def __repr__(self):
        return "*" if self.hidden else self.name
    
    def __eq__(self, other):
        return self.name == other.name and self.hidden == other.hidden

    @staticmethod
    def _random_name():
        return ''.join(random.choices(string.ascii_letters, k=5))

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**{k: data[k] for k in ("name", "hidden") & data.keys()})

    def flip(self):
        self.hidden = not self.hidden

def to_stone(arg):
    return arg if isinstance(arg, StoneClassic) else StoneClassic(name=arg)

# %%
from dataclasses import dataclass, field
import random, string

@dataclass(unsafe_hash=True)
class Stone:
    name: str = field(default_factory = lambda: Stone._random_name())
    hidden: bool = False

    def __post_init__(self):
        if not isinstance(self.name, str):
            self.name = self._random_name()

    def __repr__(self):
        return "*" if self.hidden else self.name
    
    @staticmethod
    def _random_name():
        return ''.join(random.choices(string.ascii_letters, k=5))

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**{k: data[k] for k in cls.__dataclass_fields__ & data.keys()})

    def flip(self):
        self.hidden = not self.hidden

def to_stone(arg):
    return arg if isinstance(arg, Stone) else Stone(name=arg)

# %%
class Reserve(set):
    def __init__(self, *args, length=6):
        super().__init__((to_stone(arg) for arg in args) if args else map(to_stone, range(length)))
    def remove_stone(self, element):
        return super().remove(to_stone(element))

# %%
class Board(list):
    def __init__(self, *args, length=1):
        super().__init__(map(to_stone, args) if args else map(to_stone, range(length)))

    def peek(self, *args):
        return (self[i-1].name for i in args) if args else (s.name for s in self)

    def place(self, stone, position="right"):
        self.append(to_stone(stone)) if position == "right" else self.insert(0, to_stone(stone))

# %%
b = Board(length=3)
b.peek()
b[0].flip()
b
b.peek(1,3)

# %%
class TellStones:
    def __init__(self, board:Board = Board(), reserve:Reserve = Reserve()):
        self.board = board
        self.reserve = reserve
    def __repr__(self):
        return f"Board: {self.board}\nReserve: {self.reserve}"

# %% [markdown]
# !pip install nbimporter


