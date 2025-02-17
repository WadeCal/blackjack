from card import Card
from random import shuffle
from typing import List


class Deck:
    deckMapping = {
        "A": [1, 11],
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
    }

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self):
        self.deck: List[Card] = [
            Card(name, suit, value)
            for suit in Deck.suits
            for name, value in Deck.deckMapping.items()
        ]
        shuffle(self.deck)

    def drawCard(self) -> Card:
        return self.deck.pop() if self.deck else None

    def getDeckSize(self) -> int:
        return len(self.deck)

    def __str__(self) -> str:
        return "\n".join(str(card) for card in self.deck)
