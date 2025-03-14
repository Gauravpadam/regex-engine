from typing import *
from abc import abstractmethod, ABC
from enum import Enum

class Unit(ABC):
    """Smallest unit the AST"""
    pass

class Composite(Unit):
    """Combination of units"""
    @property
    @abstractmethod
    def children(self) -> List[Unit]:
        pass

class AST:
    """Holds the entire AST"""
    def __init__(self, is_from_start_of_string: bool,  root: Unit):
        self.is_from_start_of_string = is_from_start_of_string
        self.root = root

    def __str__(self) -> str:
        output = []
        self._visit(self.root, 0, lambda unit, level: output.append(" " * (level * 2) + "- " + self.description_for(unit)))
        return "\n".join(output)
    
    def description_for(self, unit: Unit) -> str:
        # For now, simply use the string conversion of the unit.
        return str(unit)
    
    def visit(self,  closure: Callable[[Unit], None]) -> None:
        self._visit(self.root, 0, lambda unit, level: closure(unit))
    
    def _visit(self, unit: Unit, level: int, closure: Callable[[Unit], None]):
        closure(unit, level)
        if isinstance(unit, Composite):
            for child in unit.children:
                self._visit(child, level + 1, closure)

class Group(Composite):
    def __init__(self, children: List[Unit], index: Optional[int] = None, is_capturing: bool = True):
        self.index = index
        self.is_capturing = is_capturing
        self._children = children
    
    @property
    def children(self) -> List[Unit]:
        return self._children
    
    def __repr__(self) -> str:
        return f"Group(index={self.index}, is_capturing={self.is_capturing}, children={self.children!r})"

class ImplicitGroup(Composite):
    def __init__(self, children: List[Unit]):
        self._children = children
    
    @property
    def children(self) -> List[Unit]:
        return self._children
    
    def __repr__(self) -> str:
        return f"ImplicitGroup(children={self.children!r})"

class Alternation(Composite):
    def __init__(self, children: List[Unit]):
        self._children = children
    
    @property
    def children(self) -> List[Unit]:
        return self._children

    def __repr__(self) -> str:
        return f"Alternation(children={self.children!r})"


class Backreference(Unit):
    def __init__(self, index: int):
        self.index = index
    
    def __repr__(self) -> str:
        return f"Backreference(index={self.index})"


class Anchor(Enum):
    startOfString = "startOfString"
    endOfString = "endOfString"
    wordBoundary = "wordBoundary"

    def __repr__(self) -> str:
        return f"Anchor.{self.name}"

class Match(Unit):
    pass

class AnyCharacter(Match):
    def __str__(self):
        return "AnyCharacter"
    
    def __repr__(self) -> str:
        return "AnyCharacter()"


class MatchCharacter(Match):
    def __init__(self, character: str):
        self.character = character
    
    def __str__(self):
        return f"Character('{self.character}')"

    def __repr__(self):
        return f"MatchCharacter(character={self.character})"

class MatchString(Match):
    def __init__(self, string: str):
        self.string = string
    
    def __repr__(self) -> str:
        return f"MatchString(string={self.string!r})"

class MatchSet(Match):
    def __init__(self, char_set: Any):
        self.char_set = char_set
    
    def __repr__(self) -> str:
        return f"MatchSet(char_set={self.char_set!r})"

class CharacterGroupItem(ABC):
    pass

class CharacterGroup(Unit):
    def __init__(self, is_inverted: bool, items: List[CharacterGroupItem]):
        self.is_inverted = is_inverted
        self.items = items
    
    def __repr__(self) -> str:
        return f"CharacterGroup(is_inverted={self.is_inverted}, items={self.items!r})"

class GroupItemCharacter(CharacterGroupItem):
    def __init__(self, character: str):
        self.character = character

    def __repr__(self) -> str:
        return f'Character("{self.character}")'

class GroupItemRange(CharacterGroupItem):
    def __init__(self, start: str, end:str):
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f'Range({self.start}...{self.end})'

class QuantifiedExpression(Composite):
    def __init__(self, expression: Unit, quantifier: 'Quantifier'):
        self.expression = expression
        self.quantifier = quantifier
    
    @property
    def children(self) -> List[Unit]:
        return [self.expression]
    
    def __repr__(self) -> str: 
        return f"QuantifiedExpression(expression={self.expression!r}, quantifier={self.quantifier!r})"
    

class Quantifier:
    def __init__(self, qtype: 'QuantifierType', is_lazy: bool = False):
        self.qtype = qtype
        self.is_lazy = is_lazy

    def __repr__(self):
        return f"Quantifier(qtype={self.qtype}, is_lazy={self.is_lazy})"


class QuantifierType(Enum):
    ZERO_OR_MORE = "zeroOrMore"
    ONE_OR_MORE = "oneOrMore"
    ZERO_OR_ONE = "zeroOrOne"
    RANGE = "range"

    def __repr__(self) -> str:
        return f"QuantifierType.{self.name}"

class RangeQuantifier:
    def __init__(self, lower_bound: int, upper_bound: Optional[int] = None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def __repr__(self) -> str:
        return f"RangeQuantifier(lower_bound={self.lower_bound}, upper_bound={self.upper_bound})"






        


    
