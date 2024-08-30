from Cards import SpanishDeck
from Blackjack import Blackjack
from BlackjackHand import BlackjackHand, SpBlackjackHand

from WriteToFile import WriteToFile as wtf

class SpBlackjack(Blackjack):
    def __init__(self, num_decks=6):
        self.deck = SpanishDeck(num_decks)
        self.deck.shuffle()

        self.player_hands = [SpBlackjackHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackHand(self.draw_card(number_of_cards=2))

        self.hand_amount_wagered = 0.0
        self.hand_amount_won = 0.0

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    

    

if __name__ == "__main__":
    pass

