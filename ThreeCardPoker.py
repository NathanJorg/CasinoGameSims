from PokerHand import ThreeCardHand
from Cards import Deck

from pathlib import Path

import os
import pandas as pd

class ThreeCardPoker:
    ante_bonus_paytable = {
        "Straight Flush": 5,
        "Three of a Kind": 4,
        "Straight": 1,
    }
        
    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.ante_bet = 1.0
        self.play_bet = self.ante_bet

        self.player_hand = ThreeCardHand(self.draw_cards(number_of_cards=3))
        self.dealer_hand = ThreeCardHand(self.draw_cards(number_of_cards=3))

    def draw_cards(self, number_of_cards):
        return [self.deck.draw_card() for _ in range(number_of_cards)]
    
    def dealer_qualifies(self):
        return self.dealer_hand.hand_rank_value >= 2 or any(rank in self.dealer_hand.ranks for rank in [12, 13, 14])

    def player_pair_or_greater(self):
        return self.player_hand.hand_rank_value >= 2
    
    def hand_greater_than_q_6_4(self):
        if any(rank in self.player_hand.ranks for rank in [13, 14]): 
            return True
        if 12 in self.player_hand.ranks:            
            if self.player_hand.ranks[1] > 6:                
                return True
            if self.player_hand.ranks[1] == 6 and self.player_hand.ranks[2] in [4, 5]:
                return True 
            return False          
        return False

    def does_player_play(self):
        if self.player_pair_or_greater():
            return True
        
        if self.hand_greater_than_q_6_4():
            return True               
         
        return False
    
    def player_folds(self):
        return not self.does_player_play()

    def player_wins(self):
        if self.player_hand.hand_rank_value > self.dealer_hand.hand_rank_value:
            return True
        
        if self.player_hand.hand_rank_value == self.dealer_hand.hand_rank_value and self.player_hand.ranks > self.dealer_hand.ranks:
            return True

        return False
    
    def player_ties(self):
        return self.player_hand.hand_rank_value == self.player_hand.hand_rank_value and self.player_hand.ranks == self.dealer_hand.ranks

    def ante_bonus_pay(self):
        return self.ante_bonus_paytable.get(self.player_hand.hand_rank, 0)

    def amount_bet(self):
        return self.ante_bet + self.play_bet if self.does_player_play() else self.ante_bet
    
    def amount_won(self):
        if self.player_folds():
            return 0.0
        
        if not self.dealer_qualifies():
            return 2 * self.ante_bet + self.play_bet + self.ante_bonus_pay()       
        
        if self.player_wins():
            return 2 * self.ante_bet + 2 * self.play_bet + self.ante_bonus_pay()
        
        if self.player_ties():
            return self.ante_bet + self.play_bet + self.ante_bonus_pay()
            
        return 0.0 + self.ante_bonus_pay()
        
    def game_results(self):
        # return amount_bet, amount_won
        return self.amount_bet(), self.amount_won()


def write_to_file(data, filename):
    df = pd.DataFrame(data)
    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
  
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(df.to_string(index=False))

def write_to_csv(data, filename):
    df = pd.DataFrame(data)
    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(filename, sep='\t', encoding='utf-8', index=False, header=True)

def main():
    
    num_hands = 10000000
    amount_bet = 0.0
    amount_won = 0.0
    file_count = 1
    data_raw = []

    for iter in range(1, num_hands+1):
        game = ThreeCardPoker()
        amount_bet_game, amount_won_game = game.game_results()

        amount_bet += amount_bet_game
        amount_won += amount_won_game 

        new_row = {
            'Hand': iter,
            'Player hand': game.player_hand,
            'Dealer hand': game.dealer_hand,
            'Player rank': game.player_hand.hand_rank,
            'Dealer rank': None if not game.dealer_qualifies() else game.dealer_hand.hand_rank,
            'Player hand rank': game.player_hand.hand_rank_value,
            'Dealer hand rank': game.dealer_hand.hand_rank_value,
            'Amount bet': amount_bet_game,
            'Amount won': amount_won_game
        }

        data_raw.append(new_row)

        if iter % 500000 == 0:
            filename_raw = f'.\\Three Card Results\\three_card_{file_count}.txt'
            filename_csv = f'.\\Three Card Results\\three_card_csv_{file_count}.txt'

            write_to_file(data_raw, filename_raw)
            write_to_csv(data_raw, filename_csv)
            file_count += 1
            data_raw = []
            print(iter, amount_bet, ' ', amount_won, ' ', 1-amount_won/amount_bet, ' ', (amount_bet-amount_won)/iter)

    if data_raw:
        filename = f'.\\Baccarat Results\\baccarat_results_{file_count}.txt'
        write_to_file(data_raw, filename)    
    
    print(amount_bet, ' ', amount_won, ' ', 1-amount_won/amount_bet, ' ', (amount_bet-amount_won)/num_hands)

if __name__ == "__main__":

    main()