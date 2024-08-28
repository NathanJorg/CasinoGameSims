from Cards import Deck
from BlackjackHand import BlackjackHand

class BlackjackChallenge():

    def __init__(self, num_decks=6, max_hands=3):
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        
        # game attributes
        self.max_hands = max_hands

        #game initialisation
        self.game_win = 0.0

        self.player_hands = [BlackjackHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackHand(self.draw_card(number_of_cards=2))

    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
    
    def draw_card(self, number_of_cards=1):
        return [self.deck.draw_card() for _ in range(number_of_cards)]
      
    @property
    def dealer_first_card_rank(self):
        return self.dealer_hand.card_ranks[0]
    
    @property
    def money_on_table(self):
        return sum(hand.wagered_amount for hand in self.player_hands)
    
    def blackjack_pays(self, hand: BlackjackHand):
        if not self.dealer_hand.is_hand_blackjack:
            return 2.0
        if hand.blackjack_rank < self.dealer_hand.blackjack_rank:
            return 3.0
        if hand.blackjack_rank == self.dealer_hand.blackjack_rank:
            return 4.0
        if hand.blackjack_rank > self.dealer_hand.blackjack_rank:
            return 5.0 
 
    def calculate_payout(self, hand: BlackjackHand):
        if hand.is_hand_busted:
            return -1.0
        elif hand.is_hand_blackjack:
            return self.blackjack_pays(hand)
        elif hand.is_five_card_charlie:
            return 1.0
        elif hand.hand_value == 21:
            return 1.0
        elif self.dealer_hand.is_hand_busted:
            return 1.0
        elif hand.hand_value > self.dealer_hand.hand_value:
            return 1.0
        
        # all other hands lose
        return -1.0

    def dealer_play(self) -> None:
        while self.dealer_hand.hand_value < 17:
            self.dealer_hand.add_card(self.draw_card())

    def can_split(self, hand: BlackjackHand):        
        return hand.can_split
    
    def does_player_split(self, hand: BlackjackHand):
        if not self.can_split(hand):
            return False
        
        card_rank = hand.card_ranks[0]

        if card_rank == 2 and self.dealer_first_card_rank in [4, 5, 6]:
            return True
        if card_rank == 3 and self.dealer_first_card_rank in [3, 4, 5, 6, 7]:
            return True
        if card_rank == 4 and self.dealer_first_card_rank in [5, 6]:
            return True
        if card_rank == 6 and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
            return True  
        if card_rank == 7 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7]:
            return True
        if card_rank in [8, 11]:
            return True
        if card_rank == 9 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 8, 9]:
            return True
        if card_rank == 10 and self.dealer_first_card_rank == 6:
            return True
        
        return False
    
    def does_player_double(self, hand: BlackjackHand):
        if len(hand.hand) == 2 and hand.is_hand_soft:
            if hand.hand_value == 16 and self.dealer_first_card_rank in [5, 6]:
                return True
            if hand.hand_value == 17 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            if hand.hand_value == 18 and self.dealer_first_card_rank in [3, 4, 5, 6]:
                return True
            
        elif len(hand.hand) == 2 and not hand.is_hand_soft:   
            if hand.hand_value == 9 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            if hand.hand_value == 10 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8]:
                return True
            if hand.hand_value == 11 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
                return True
        
        elif len(hand.hand) == 3 and not hand.is_hand_soft:
            if hand.hand_value == 10 and self.dealer_first_card_rank in [3, 4, 5, 6]:
                return True
            if hand.hand_value == 11 and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True

        return False
    
    def does_player_stand(self, hand: BlackjackHand):
        if len(hand.hand) == 2 and hand.is_hand_soft:
            if hand.hand_value == 18 and self.dealer_first_card_rank in [7, 8]:
                return True
            if hand.hand_value >= 19:
                return True
        if len(hand.hand) == 2 and not hand.is_hand_soft:
            if hand.hand_value == 12 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            if hand.hand_value in [13, 14, 15] and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True
            if hand.hand_value == 16 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 10]:
                return True
            if hand.hand_value == 17 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 9, 10]:
                return True
            if hand.hand_value >= 18:
                return True
        
        if len(hand.hand) == 3 and hand.is_hand_soft:
            if hand.hand_value == 19 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8]:
                return True
            if hand.hand_value >= 20:
                return True
        if len(hand.hand) == 3 and not hand.is_hand_soft:
            if hand.hand_value == 13 and self.dealer_first_card_rank in [3, 4, 5, 6]:
                return True
            if hand.hand_value in [14, 15] and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True
            if hand.hand_value == 16 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 9, 10]:
                return True
            if hand.hand_value == 17 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
                return True
            if hand.hand_value >= 18:
                return True
            
        if len(hand.hand) == 4 and hand.is_hand_soft:
            if hand.hand_value == 21:
                return True
        if len(hand.hand) == 4 and not hand.is_hand_soft:
            if hand.hand_value == 16 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            if hand.hand_value == 17 and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True
            if hand.hand_value >= 18:
                return True
        
        if len(hand.hand) == 5:
            return True
        
        return False
            
    def split_player_hand(self, hand: BlackjackHand):
        new_hand = BlackjackHand([hand.hand.pop()])
        hand.add_card(self.draw_card())
        new_hand.add_card(self.draw_card())
        self.player_hands.append(new_hand)
    
    def double_down(self, hand: BlackjackHand):
        hand.wagered_amount *= 2
        hand.add_card(self.draw_card())
    
    def optimal_strategy(self, hand: BlackjackHand):
        while True:
            if self.does_player_split(hand) and len(self.player_hands) < self.max_hands:
                self.split_player_hand(hand)
            elif self.does_player_double(hand):
                self.double_down(hand)
                break
            elif self.does_player_stand(hand):
                break
            else:
                hand.add_card(self.draw_card())  

    def play(self):
        hand_index = 0
        while hand_index < len(self.player_hands):
            self.optimal_strategy(self.player_hands[hand_index])
            hand_index += 1
        
    def is_hand_auto_resolved(self, hand: BlackjackHand):
        if hand.is_hand_blackjack:
            return True
        if hand.is_five_card_charlie:
            return True
        if hand.hand_value == 21:
            return True
        if hand.is_hand_busted:
            return True
        return False
    
    def amount_not_auto_resolved(self):       
        return sum(hand.wagered_amount for hand in self.player_hands if not self.is_hand_auto_resolved(hand))


    def win(self):
        
        unresolved_amount = self.amount_not_auto_resolved()

        for hand in self.player_hands:
            if self.is_hand_auto_resolved(hand):
                self.set_hand_winnings(hand)
            elif self.dealer_hand.is_hand_blackjack:  
                unresolved_amount = self.handle_blackjack_unresolved(hand, unresolved_amount)
            else:
                self.set_hand_winnings(hand)

    def set_hand_winnings(self, hand: BlackjackHand):
        hand.amount_won = hand.wagered_amount * self.calculate_payout(hand)

    def handle_blackjack_unresolved(self, hand: BlackjackHand, unresolved_amount):

        if unresolved_amount > hand.wagered_amount:
            unresolved_amount -= hand.wagered_amount
        else:
            if hand.has_doubled:
                hand.wagered_amount = 1.0
            self.set_hand_winnings(hand)

        return unresolved_amount

if __name__ == "__main__":

    num_hands = 1000000

    amount_won = 0
    amount_bet = 0

    for iter in range(1, num_hands+1):
        game = BlackjackChallenge()
        game.play()
        game.dealer_play()
        game.win()

        amount_won_hand = sum(hand.amount_won for hand in game.player_hands)
        amount_bet_hand = sum(hand.wagered_amount for hand in game.player_hands)

        amount_won += amount_won_hand
        amount_bet += amount_bet_hand

    print(num_hands, ' ', amount_bet, ' ', amount_won, ' ', amount_won/num_hands)
