from abc import abstractmethod, ABC
from typing import *

class Cursor:
    """
    Cursor represents the input string and the current position in the string.
    It also keeps track of capture groups and the index of the previous match.
    """
    def __init__(self, string: str):
        self.string: str = string
        self.start_index: int = 0  # Start of search
        self.end_index: int = len(string)  # End index of the string
        self.index: int = 0  # Current position of the cursor
        self.groups: Dict[int, Tuple[int, int]] = {}  # Maps group numbers to (start, end) indices
        self.previous_match_index: Optional[int] = None
    
    # Cursor starts moving
    def start_at(self, index: int) -> None:
        """Resets the cursor to the given index and clears captured groups"""
        self.start_index: int = index
        self.index = index
        self.groups.clear()
    
    def advance_to(self, index: int) -> None:
        """Move current index to the given index"""
        self.index = index
    
    def advance_to_end_of_match(self, match: 'RegexMatch'):
        """
        Advances the cursor to the end of the match.
        """
        pass
        # TODO: POST matcher.py
    
    # Characters

    def __getitem__(self, key):
        return self.string[key]
    
    @property
    def character(self) -> Optional[str]:
        """Return the character with the current index, or none if at the end"""
        return self.string[self.index] if self.index < self.end_index else None
    
    def character_offset_by(self, offset: int) -> str:
        """Returns the character at an offset from the current index"""
        return self.string[self.index + offset]
    
    # Indices

    def index_offset_by(self, offset: int) -> Optional[int]:
        """
        Returns the index offset by 'offset' from the current index, or none if
        it goes beyond the string
        """

        new_index = self.index + offset

        return new_index if new_index < self.end_index else None
    
    def index_after(self, index: int) -> int:
        """Returns index immediately after given index"""
        return index + 1
    
    @property
    def is_empty(self) -> bool:
        """Returns True if there are no more characters to match"""
        return self.index >= self.end_index
    
    @property
    def is_at_last_index(self) -> bool:
        """
        Returns True if the current index is at the last character.
        Note: This is True only if there is exactly one character remaining.
        """
        return self.index < self.end_index and (self.index + 1 == self.end_index)
    
    def __str__(self) -> str:
        """
        Returns description of the cursor
        current index(as an offset from the start) and the current character
        """
        ch = self.character if self.character is not None else "phi"
        if ch == "\n":
            ch = "\\n"
        
        return f"{self.index}, {ch}"

class RegexMatch:
    pass
