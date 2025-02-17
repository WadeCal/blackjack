from deck import Deck


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
