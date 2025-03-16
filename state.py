from abc import ABC, abstractmethod
from typing import *
from cursor import Cursor

class State:
    """
    A State for the state machine
    """
    def __init__(self):
        self.transition: List['Transition'] = []
    
    def __hash__(self) -> int:
        # Use the unique object id for hashing
        return hash(id(self))
    
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, State) and id(self) == id(other)
    
    def __repr__(self) -> str:
        return f"<State id={id(self)} transition={len(self.transition)}>"

class Transition:
    """
    A transition between two states of a state machine
    """
    def __init__(self, end: State, condition: 'Condition'):
        self.end = end
        self.condition = condition
    
    @property
    def is_unconditional_epsilon(self) -> bool:
        """
        If this is an unconditional transition, this functional will return a true
        """
        if isinstance(self.condition, 'Epsilon'):
            return self.condition.predicate is None
        return False
    
    @staticmethod
    def epsilon(end: State, condition: Optional[Callable[[Cursor], bool]] = None) -> 'Transition':
        """
        Creates a transition which won't consume any characters
        """
        return Transition(end, Epsilon(condition))

    def __repr__(self) -> str:
        cond_repr = repr(self.condition)
        return f"<Transition to State(id={id(self.end)}) with {cond_repr}"

class Condition(ABC):
    @abstractmethod
    def can_perform_transition(self, cursor: Cursor) -> 'ConditionResult':
        """
        Determines if a transtiton is possibe in the given context
        Returns a ConditionResult:
            - accepted(count) when accepted, consuming 'count' characters
            - rejected otherwise
        """
        pass

class ConditionResult:
    def __init__(self, accepted: bool, count: int = 1):
        self.accepted = accepted
        self.count = count
    
    @classmethod
    def accepted_result(cls, count: int = 1) -> 'ConditionResult':
        return cls(True, count)
    
    @classmethod
    def rejected_result(cls) -> 'ConditionResult':
        return cls(False)
    
    def __repr__(self) -> str:
        if self.accepted:
            return f"accepted(count={self.count})"
        return "rejected"

class Epsilon(Condition):
    """
    An Epsilon condition represents a transition which does not consume any characters
    If a predicate is provided it must return true for the transition to be accepted
    """
    def __init__(self, predicate: Optional[Callable[[Cursor], bool]] = None):
        self.predicate = predicate
    

    def can_perform_transition(self, cursor: Cursor) -> ConditionResult: 
        if self.predicate is not None:
            return ConditionResult.accepted_result(count = 0) if self.predicate(cursor) else ConditionResult.rejected_result()
        return ConditionResult.accepted_result(count = 0)
    
    def __repr__(self) -> str:
        if self.predicate:
            return f"Epsilon(predicate={self.predicate})"
        return "Epsilon()"

class MatchChar(Condition):
    """
    If a match occurs, we transition the state of the matchine
    """
    def __init__(self, char: str):
        self.char = char
    
    def can_perform_transition(self, cursor: Cursor) -> ConditionResult:
        """Checks if a transition is possible based on cursor's current character"""
        
        if cursor.character == self.char:
            return ConditionResult.accepted_result(count=1)
        return ConditionResult.rejected_result()
    
    def __repr__(self):
        return f"MatchChar('{self.char}')"

class AnyCharacter(Condition):

    def __init__(self, including_newline: bool = True):
        self.including_newline = including_newline
    
    def can_perform_transition(self, cursor: Cursor) -> ConditionResult:
        if cursor.is_empty:
            return ConditionResult.rejected_result()
        if not self.including_newline and cursor.character == "\n":
            return ConditionResult.rejected_result()
        return ConditionResult.accepted_result(count=1)

    def __repr__(self) -> str:
        return f"AnyCharacter(including_newline={self.including_newline})"

    
    


    

        