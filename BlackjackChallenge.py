from Cards import Deck
from BlackjackHand import BlackjackHand

class BlackjackChallenge():

    def __init__(self, num_decks=6, bet=1.0, max_hands=3):
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        
        # game attributes
        self.bet = bet
        self.max_hands = max_hands

        #game initialisation
        self.player_bet = []
        self.amount_won = 0.0

        self.hands = [BlackjackHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackHand(self.draw_card(number_of_cards=2))

    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
    
    def draw_card(self, number_of_cards=1):
        return [self.deck.draw_card() for _ in range(number_of_cards)]
    
    @property
    def dealer_first_card_rank(self):
        return self.dealer_hand.card_ranks[0]
    
    def five_card_charlie(self, hand: BlackjackHand):
        return len(hand.hand) == 5 and hand.hand_value <= 21

    def dealer_play(self) -> None:
        while self.dealer_hand.hand_value < 17:
            self.dealer_hand.add_card(self.draw_card())

    def can_split(self, hand: BlackjackHand):        
        return hand.can_split()
    
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
        
        return False
            


    def split_player_hand(self, hand: BlackjackHand):
        new_hand = BlackjackHand([hand.hand.pop()])
        hand.add_card(self.draw_card())
        new_hand.add_card(self.draw_card())
        self.hands.append(new_hand)
    
    def double_down(self, hand: BlackjackHand):
        hand.add_card(self.draw_card())

    
    def optimal_strategy(self, hand: BlackjackHand):
        while True:
            if self.does_player_split(hand) and len(self.hands) < self.max_hands:
                self.split_player_hand(hand)
                print('split')
            elif self.does_player_double(hand):
                self.double_down(hand)
                print('double')
                break
            elif self.does_player_stand(hand):
                print('stand')
                break
            else:
                print('hit')
                hand.add_card(self.draw_card())  

    def play(self):
        hand_index = 0
        while hand_index < len(self.hands):
            self.optimal_strategy(self.hands[hand_index])
            hand_index += 1





game = BlackjackChallenge()

game.play()
game.dealer_play()

print(game.hands[0])
print(game.dealer_hand)
