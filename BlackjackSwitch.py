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

        #self.hand_one_strength = self.evaluate_hand_strength(self.player_hand_one[0])
        #self.hand_two_strength = self.evaluate_hand_strength(self.player_hand_two[0])

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

    def evaluate_hand_strength(self, hand: BlackjackSwitchHand):
        # Custom rules
        # print(hand)
        print(hand.hand_value)

        if hand.hand_value == 21:
            return 10
        if hand.hand_value == 20:
            return 9
        if hand.hand_value == 19:
            return 8
        if [hand.hand[0].rank, hand.hand[1].rank] == ['A', 'A']:
            return 7.5
        if hand.hand_value == 11:
            return 7
        if hand.hand_value == 10:
            return 6
        if hand.hand_value == 9:
            return 5
        if hand.hand_value == 18 or hand.hand_value == 8:
            return 4
        if [hand.hand[0].rank, hand.hand[1].rank] == ['8', '8'] and 2 <= self.dealer_first_card_value <= 8:
            return 3.5
        return 0
    
    def evaluate_hand_second_check(self, hand: BlackjackSwitchHand):
        if hand.hand_value == 17 or hand.hand_value == 7:
            return 3
        if self.does_player_split(hand):
            return 2
        if hand.hand_value == 12:
            return 1.5
        if hand.hand_value == 13:
            return 1
        return 0
    
    def does_player_split(self, hand: BlackjackSwitchHand):
        if not hand.can_split:
            return False
        
        card_rank = hand.card_ranks[0]

        if card_rank in [2, 3] and self.dealer_first_card_value in [5, 6, 7]:
            return True
        if card_rank == 6 and self.dealer_first_card_value in [4, 5, 6]:
            return True  
        if card_rank == 7 and self.dealer_first_card_value in [3, 4, 5, 6, 7]:
            return True
        if card_rank == 8 and self.dealer_first_card_value in [2, 3, 4, 5, 6, 7, 8, 9]: 
            return True
        if card_rank == 9 and self.dealer_first_card_value in [4, 5, 6, 8, 9]:
            return True
        if card_rank == 11:
            return True
        
        return False
    
    def check_exceptions(self, hand):
        if sorted(hand) == [3, 8]:
            return True
        if sorted(hand) == [2, 9] and self.dealer_first_card_value in [2, 3, 4, 5, 6]:
            return True
        if sorted(hand) == [2, 8]: 
            return True
        return False

    def simple_switching_strategy(self):

        # Keep original hands
        original_hand_one = self.player_hand_one[0]
        original_hand_two = self.player_hand_two[0]

        hand_one_ranks = [original_hand_one.card_ranks[0], original_hand_one.card_ranks[1]]
        hand_two_ranks = [original_hand_two.card_ranks[0], original_hand_two.card_ranks[1]]

        # Exception handling for AA + 3,8 or AA + 2,9 or AA + 2,8
        if not (hand_one_ranks == [11, 11] and self.check_exceptions(hand_two_ranks)) or (hand_two_ranks == [11, 11] and self.check_exceptions(hand_one_ranks)):

            # Try original and switched hands
            switched_hand_one = BlackjackSwitchHand([original_hand_one.hand[0], original_hand_two.hand[1]])
            switched_hand_two = BlackjackSwitchHand([original_hand_two.hand[0], original_hand_one.hand[1]])


            if self.dealer_first_card_value in [7, 8]:
                # Balance the hands: prioritize weakest hand being stronger
                orig_weak = min(
                    self.evaluate_hand_strength(original_hand_one),
                    self.evaluate_hand_strength(original_hand_two)
                )
                switch_weak = min(
                    self.evaluate_hand_strength(switched_hand_one),
                    self.evaluate_hand_strength(switched_hand_two)
                )
                if switch_weak > orig_weak:
                    print(self.player_hand_one[0])
                    self.player_hand_one[0] = switched_hand_one
                    self.player_hand_two[0] = switched_hand_two
                    print(self.player_hand_one[0])

            else:
                # Maximize the strongest hand
                orig_strong = max(
                    self.evaluate_hand_strength(original_hand_one),
                    self.evaluate_hand_strength(original_hand_two)
                )
                switch_strong = max(
                    self.evaluate_hand_strength(switched_hand_one),
                    self.evaluate_hand_strength(switched_hand_two)
                )
                if switch_strong > orig_strong:
                    print(self.player_hand_one[0])
                    self.player_hand_one[0] = switched_hand_one
                    self.player_hand_two[0] = switched_hand_two
                    print(self.player_hand_one[0])
        
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

    # hand_one_card_one = game.player_hand_one[0].card_ranks[0]
    # hand_one_card_two = game.player_hand_one[0].card_ranks[1]

    # hand_two_card_one = game.player_hand_two[0].card_ranks[0]
    # hand_two_card_two = game.player_hand_two[0].card_ranks[1]

    # total_one = game.calculate_hand_points(hand_one_card_one, hand_one_card_two) + game.calculate_hand_points(hand_two_card_one, hand_two_card_two)
    # total_two = game.calculate_hand_points(hand_one_card_one, hand_two_card_two) + game.calculate_hand_points(hand_two_card_one, hand_one_card_two)

    game.simple_switching_strategy()


if __name__ == "__main__":
    main()