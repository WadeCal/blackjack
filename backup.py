"""This file is just a backup containing the entire codebase, use main.py to run the game!"""

from random import shuffle
from typing import List, Union


class Card:
    def __init__(self, name: str, suit: str, value: Union[int, List[int]]):
        self.name = name
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        return f"{self.name} of {self.suit}"


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


class Player:
    def __init__(self, deck: Deck, balance: int = 100):
        self.balance = balance
        self.bet = 0
        self.deck = deck
        self.hand = []
        self.resetHand()

    def __str__(self) -> str:
        return "Hand: " + ", ".join(str(card) for card in self.hand)

    def addWinnings(self, winnings: int):
        self.balance += winnings

    def placeBet(self, bet: int):
        if 0 < bet <= self.balance:
            self.balance -= bet
            self.bet = bet
        else:
            raise ValueError("Invalid bet amount.")

    def drawCard(self):
        card = self.deck.drawCard()
        if card:
            self.hand.append(card)

    def getHandValue(self) -> int:
        total = 0
        aces = 0

        for card in self.hand:
            if isinstance(card.value, list):
                aces += 1
                total += 11  # Assume Ace as 11 first
            else:
                total += card.value

        while total > 21 and aces > 0:
            total -= 10  # Convert an Ace from 11 to 1
            aces -= 1

        return total

    def isBust(self) -> bool:
        return self.getHandValue() > 21

    def isBlackjack(self) -> bool:
        return self.getHandValue() == 21 and len(self.hand) == 2

    def resetHand(self):
        self.hand = []
        self.drawCard()
        self.drawCard()


class Game:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Player(self.deck)
        self.player = Player(self.deck)

    def displayHand(self, player: Player, isDealer: bool):
        hand = " | ".join(str(card) for card in player.hand)
        print(
            f"{'Dealer' if isDealer else 'Player'} hand: {hand} (Value: {player.getHandValue()})"
        )

    def play(self):
        while self.player.balance > 0:
            try:
                bet = int(
                    input(f"Current Balance: ${self.player.balance}.\nEnter bet: ")
                )
                self.player.placeBet(bet)
            except ValueError:
                print("Invalid bet. Try again.")
                continue

            self.player.resetHand()
            self.dealer.resetHand()
            self.displayHand(self.player, False)
            self.displayHand(self.dealer, True)
            print(f"Cards remaining in deck: {self.deck.getDeckSize()}")

            # Player's turn
            while not self.player.isBust():
                if self.player.getHandValue() == 21:
                    print("You got 21! Automatic win.")
                    break
                action = input("Draw (D) or Stand (S)? ").strip().lower()
                if action == "d":
                    self.player.drawCard()
                    self.displayHand(self.player, False)
                    print(f"Cards remaining in deck: {self.deck.getDeckSize()}")
                    if self.player.isBust():
                        print("You busted!")
                elif action == "s":
                    break
                else:
                    print("Invalid action.")

            # Dealer's turn
            if not self.player.isBust() and self.player.getHandValue() < 21:
                while self.dealer.getHandValue() < 17:
                    self.dealer.drawCard()
                    self.displayHand(self.dealer, True)
                    print(f"Cards remaining in deck: {self.deck.getDeckSize()}")

            self.displayHand(self.dealer, True)

            # Determine winner
            playerValue = self.player.getHandValue()
            dealerValue = self.dealer.getHandValue()

            if self.player.isBust():
                print("You lost!")
            elif self.dealer.isBust() or playerValue > dealerValue:
                winnings = self.player.bet * (2.5 if self.player.isBlackjack() else 2)
                print(f"You won! Winnings: {winnings}")
                self.player.addWinnings(winnings)
            elif playerValue == dealerValue:
                print("It's a tie! Bet returned.")
                self.player.addWinnings(self.player.bet)
            else:
                print("Dealer wins!")

            self.player.bet = 0
            if self.player.balance == 0:
                break

            if input("Play again? (Y/N) ").strip().lower() != "y":
                break

        print("Game over! Your final balance was $", self.player.balance)
