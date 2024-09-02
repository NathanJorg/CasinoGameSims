from Cards import Deck
from BaccaratHand import BaccaratHand

class Baccarat:
    def __init__(self, decks=8, no_commission=False):
        self.deck = Deck(decks)
        self.deck.shuffle()
        self.no_commission = no_commission

        self.player_hand = BaccaratHand(self.draw_card(number_of_cards=2))
        self.banker_hand = BaccaratHand(self.draw_card(number_of_cards=2))

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
       
    def winner_pay(self):
        if self.player_hand.hand_value == self.banker_hand.hand_value:
            return 1.0, 1.0, 9.0
        elif self.player_hand.hand_value > self.banker_hand.hand_value:
            return 0.0, 2.0, 0.0
        
        # banker win
        elif self.no_commission:
            if self.banker_hand.hand_value == 6:
                return 1.5, 0.0, 0.0
            else:
                return 2.0, 0.0, 0.0
        else:
            return 1.95, 0.0, 0.0
        
    def is_natural_hand(self):
        return self.player_hand.hand_value in [8, 9] or self.banker_hand.hand_value in [8, 9]
    
    def banker_draws_third_card(self):
        if self.banker_hand.hand_value == 6 and self.player_hand.third_card_value in [6, 7]:
            return True
        if self.banker_hand.hand_value == 5 and self.player_hand.third_card_value in [4, 5, 6, 7]:
            return True
        if self.banker_hand.hand_value == 4 and self.player_hand.third_card_value in [2, 3, 4, 5, 6, 7]:
            return True
        if self.banker_hand.hand_value == 3 and self.player_hand.third_card_value in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
            return True
        if self.banker_hand.hand_value in [0, 1, 2]:
            return True
        return False
        
    def game_winnings(self):
        self.banker_win, self.player_win, self.tie_win = self.winner_pay()
    
    def play(self) -> None:
        if self.is_natural_hand():
            pass

        elif self.player_hand.hand_value in [6, 7] and self.banker_hand.hand_value <= 5:
            self.banker_hand.add_card(self.deck.draw_card())

        elif self.player_hand.hand_value  <= 5:
            self.player_hand.add_card(self.deck.draw_card())

            if self.banker_draws_third_card():
                self.banker_hand.add_card(self.deck.draw_card()) 

if __name__ == "__main__":

    num_hands = 50000000
    amount_bet = 0
    amount_won = 0

    banker_win = 0
    player_win = 0
    tie_win = 0
    
    for iter in range(1, num_hands+1):
        game = Baccarat()
        game.play()
        game.game_winnings()
    
        banker_win += game.banker_win
        player_win += game.player_win
        tie_win += game.tie_win
        
        if iter % 500000 == 0:
            print(iter, ' ', banker_win, ' ', player_win, ' ', tie_win, ' ', banker_win/iter, ' ', player_win/iter, ' ', tie_win/iter)

    # print(num_hands, ' ', amount_bet, ' ', amount_won, ' ', amount_won/amount_bet, amount_won/num_hands)
    
        