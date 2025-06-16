from BlackjackHand import BlackjackSwitchDealerHand, BlackjackSwitchHand
from Cards import Deck
from blackjack_switch_strategy import *

class BlackjackSwitch():
    def __init__(self, num_decks=6, max_hands=2):
        self.deck = Deck(num_decks)
        self.deck.shuffle()

        self.max_hands = max_hands

        self.player_hands_one = [BlackjackSwitchHand(self.draw_card(number_of_cards=2))]
        self.player_hands_two = [BlackjackSwitchHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackSwitchDealerHand(self.draw_card(number_of_cards=2))

        self.hand_amount_wagered = 0.0
        self.hand_amount_won = 0.0

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    @property
    def dealer_first_card_value(self):
        return self.dealer_hand.card_ranks[0]
    
    