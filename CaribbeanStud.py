from PokerHand import PokerHand
from Cards import Deck

from WriteToFile import WriteToFile as wtf

class CarribeanStud:

    raise_pay_table = {
        "Royal Flush": 100,
        "Straight Flush": 50,
        "Four of a Kind": 20,
        "Full House": 7,
        "Flush": 5,
        "Straight": 4,
        "Three of a Kind": 3,
        "Two Pair": 2,
        "One Pair": 1,
        "High Card": 1
    }

    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.ante = 1.0
        self.raise_bet = 2*self.ante

        self.player_hand = PokerHand(self.draw_cards(number_of_cards=5))
        self.dealer_hand = PokerHand(self.draw_cards(number_of_cards=5))

    @property
    def dealer_up_card_rank(self):
        dealer_up_card = self.dealer_hand.hand[0]
        return PokerHand.rank_values[dealer_up_card.rank]

    def draw_cards(self, number_of_cards):
        return [self.deck.draw_card() for _ in range(number_of_cards)]
    
    def does_dealer_qualify(self):
        return self.dealer_hand.hand_rank_value >= 2 or (14 in self.dealer_hand.ranks and 13 in self.dealer_hand.ranks)
    
    def does_player_raise_optimal(self): 
        pass # wip

    def does_player_raise_basic(self):
        if self.player_hand.hand_rank_value >= 2:
            return True
                
        if 14 in self.player_hand.ranks and 13 in self.player_hand.ranks: #player has A-K
            if self.dealer_up_card_rank in self.player_hand.ranks:
                return True
            if self.dealer_up_card_rank in [14, 13] and (12 in self.player_hand.ranks or 11 in self.player_hand.ranks):
                return True
            if 12 in self.player_hand.ranks and self.dealer_up_card_rank < self.player_hand.ranks[3]:
                return True
            
        return False
    
    def does_player_fold(self):
        return not self.does_player_raise_basic()

    def does_player_win(self):
        if self.player_hand.hand_rank_value > self.dealer_hand.hand_rank_value:
            return True
        
        if self.player_hand.hand_rank_value == self.dealer_hand.hand_rank_value and self.player_hand.ranks > self.dealer_hand.ranks:
            return True

        return False
    
    def does_player_tie(self):
        return self.player_hand.hand_rank_value == self.player_hand.hand_rank_value and self.player_hand.ranks == self.dealer_hand.ranks
    
    def amount_bet(self):
        return self.ante + self.raise_bet if self.does_player_raise_basic() else self.ante

    def amount_won(self):
        if self.does_player_fold():
            return -1.0
        
        if not self.does_dealer_qualify():
            return self.ante
        
        if self.does_player_win():
            return self.ante + self.raise_bet * self.raise_pay_table[self.player_hand.hand_rank]
        
        if self.does_player_tie():
            return 0.0
    
        return -1.0 * (self.ante + self.raise_bet)
        
    def game_results(self):
        # return amount_bet, amount_won
        return self.amount_bet(), self.amount_won()
        

if __name__ == "__main__":

    num_hands = 2000000
    amount_bet = 0
    amount_won = 0
    
    data = []
    file_count = 1

    data_headers = [ 
        'Hand', 
        'Player Hand',
        'Dealer Hand',
        'Player Rank',
        'Dealer Rank',
        'Amount Bet',
        'Amount Won'
    ]
    data_raw = []

    for iter in range(1, num_hands+1):
        game = CarribeanStud()
    
        amount_bet_game, amount_won_game = game.game_results()

        amount_bet += amount_bet_game
        amount_won += amount_won_game

        new_row = {
            'Hand': iter,
            'Player Hand': game.player_hand,
            'Dealer Hand': game.dealer_hand,
            'Player Rank': game.player_hand.hand_rank,
            'Dealer Rank': game.dealer_hand.hand_rank if game.does_dealer_qualify() else None,
            # 'Player hand rank': game.player_hand.hand_rank_value,
            # 'Dealer hand rank': game.dealer_hand.hand_rank_value,
            'Amount Bet': amount_bet_game,
            'Amount Won': amount_won_game
        }

        data_raw.append(new_row)
        
        if iter % 100000 == 0:
            filename_raw = f'.\\Caribbean Stud Results\\three_card_{file_count}.txt'
            filename_csv = f'.\\Caribbean Stud Results\\three_card_csv_{file_count}.csv'
            wtf.write_to_file(data_raw, filename_raw, data_headers)
            wtf.write_to_csv(data_raw, filename_csv, data_headers, empty_fields=None)
            file_count += 1
            data_raw = []

            print(f'{iter}  {amount_bet}  {amount_won}  {amount_won/amount_bet:.6f}  {amount_won/iter:.6f}')
    
    if data_raw:
        filename_raw = f'.\\Three Card Results\\three_card_{file_count}.txt'
        filename_csv = f'.\\Three Card Results\\three_card_csv_{file_count}.csv'
        wtf.write_to_file(data_raw, filename_raw, data_headers)    
        wtf.write_to_csv(data_raw, filename_csv, data_headers)

    print(f'{num_hands}  {amount_bet}  {amount_won}  {amount_won/amount_bet:.6f}  {amount_won/num_hands:.6f}')