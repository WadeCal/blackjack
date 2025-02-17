from deck import Deck
from player import Player


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
