from typing import List, Union


class Card:
    def __init__(self, name: str, suit: str, value: Union[int, List[int]]):
        self.name = name
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"
