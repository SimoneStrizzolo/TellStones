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
        print(*(self[i-1].name for i in args)) if args else print(*(s.name for s in self))

    def place(self, stone, pos="right"):
        self.append(to_stone(stone)) if pos == "right" else self.insert(0, to_stone(stone))
    
    def swap(self, pos1, pos2):
        self[pos1-1], self[pos2-1] = self[pos2-1], self[pos1-1]

# %%
class TellStones:
    def __init__(self, board:Board = Board(), reserve:Reserve = Reserve()):
        self.board = board
        self.reserve = reserve
    
    def __repr__(self):
        return f"Board: {self.board}\nReserve: {self.reserve}"

# %%
def challenge(brd:Board, pos:int):
    guess = input(f"What's under stone {pos}? ")
    if guess == brd[pos-1].name:
        print("Correct!")
        return True
    else:
        print("Wrong!")
        return False
    
def boast(brd:Board):
    print("I know where all the stones are!")


