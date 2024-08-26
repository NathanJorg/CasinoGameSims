from PokerHand import PokerHand
from Cards import Deck

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
        return self.dealer_hand.hand_rank_value>=2 or (14 in self.dealer_hand.ranks and 13 in self.dealer_hand.ranks)
    
    def does_player_raise_optimal(self): 
        pass # wip

    def does_player_raise_basic(self):
        if self.player_hand.hand_rank_value >= 2:
            return True
                
        if 14 in self.player_hand.ranks and 13 in self.player_hand.ranks: #player has A-K
            if self.dealer_up_card_rank in self.player_hand.ranks:
                return True
            elif self.dealer_up_card_rank in [14, 13] and (12 in self.player_hand.ranks or 11 in self.player_hand.ranks):
                return True
            elif 12 in self.player_hand.ranks and self.dealer_up_card_rank < self.player_hand.ranks[3]:
                return True
            
        return False
    
    def does_player_win(self):
        if self.player_hand.hand_rank_value > self.dealer_hand.hand_rank_value:
            return True
        
        if self.player_hand.hand_rank_value == self.dealer_hand.hand_rank_value and self.player_hand.ranks > self.dealer_hand.ranks:
            return True

        return False
    
    def amount_bet(self):
        return self.ante + self.raise_bet if self.does_player_raise_basic() else self.ante

    def amount_won(self):
        if not self.does_player_raise_basic():
            return 0.0
        
        if not self.does_dealer_qualify():
            return 2 * self.ante
        
        if self.does_player_win():
            return 2 * self.ante + self.raise_bet * self.raise_pay_table[self.player_hand.hand_rank] + self.raise_bet
    
        return 0.0
        
    def game_results(self):
        # return amount_bet, amount_won
        return self.amount_bet(), self.amount_won()
        
count = 1

while True:
    game = CarribeanStud()

    if game.does_dealer_qualify() and game.player_hand.hand_rank_value == 8:

        print(game.player_hand)
        print(game.dealer_hand)

        print(game.does_dealer_qualify())

        print(game.game_results())

        print(count)

        break

    count += 1