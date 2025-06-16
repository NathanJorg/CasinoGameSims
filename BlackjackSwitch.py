from BlackjackHand import BlackjackSwitchDealerHand, BlackjackSwitchHand
from Cards import Deck
from blackjack_switch_strategy import *

class BlackjackSwitch():
    def __init__(self, num_decks=6, max_hands=2):
        self.deck = Deck(num_decks)
        self.deck.shuffle()

        self.max_hands = max_hands

        self.player_hand_one = [BlackjackSwitchHand(self.draw_card(number_of_cards=2))]
        self.player_hand_two = [BlackjackSwitchHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackSwitchDealerHand(self.draw_card(number_of_cards=2))

        self.hand_amount_wagered = 0.0
        self.hand_amount_won = 0.0

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    @property
    def dealer_first_card_value(self):
        return self.dealer_hand.card_ranks[0]
    
    def calculate_hand_points(self, card_one, card_two):
        if card_one == card_two and card_one != 10:
            value_list = VALUE_HAND_PAIR.get(self.dealer_first_card_value, {})
            return value_list.get(card_one, 0)
        if card_one == 11:
            value_list = VALUE_HAND_ACE.get(self.dealer_first_card_value, {})
            return value_list.get(card_two, 0)       
        if card_two == 11:
            value_list = VALUE_HAND_ACE.get(self.dealer_first_card_value, {})
            return value_list.get(card_one, 0)  
        else:
            hand_value = card_one + card_two
            value_list = VALUE_HAND.get(self.dealer_first_card_value, {})
            return value_list.get(hand_value, 0) 

    def simple_strategy():
        pass
    
    def calculate_payout(self, hand: BlackjackSwitchHand):
        if hand.is_hand_busted:
            return -1.0
        elif hand.is_hand_blackjack:
            return 1.0 if not self.dealer_hand.is_hand_blackjack else 0.0
        elif self.player_wins(hand):
            return 1.0
        elif self.player_ties(hand):
            return 0.0
       
        # all other hands lose
        return -1.0


def main():
    game = BlackjackSwitch()

    hand_one_card_one = game.player_hand_one[0].card_ranks[0]
    hand_one_card_two = game.player_hand_one[0].card_ranks[1]

    hand_two_card_one = game.player_hand_two[0].card_ranks[0]
    hand_two_card_two = game.player_hand_two[0].card_ranks[1]

    total_one = game.calculate_hand_points(hand_one_card_one, hand_one_card_two) + game.calculate_hand_points(hand_two_card_one, hand_two_card_two)
    total_two = game.calculate_hand_points(hand_one_card_one, hand_two_card_two) + game.calculate_hand_points(hand_two_card_one, hand_one_card_two)


if __name__ == "__main__":
    main()