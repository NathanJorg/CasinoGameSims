from Cards import Deck
from BaccaratHand import BaccaratHand, LuckyDrawHand

class LuckyDrawBaccarat:
    def __init__(self, decks=8):
        self.deck = Deck(decks)
        self.deck.shuffle()
 
        self.player_hand = LuckyDrawHand(self.draw_card(number_of_cards=2))
        self.banker_hand = BaccaratHand(self.draw_card(number_of_cards=2))

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
    
    @property
    def banker_first_card_rank(self):
        return self.banker_hand.card_ranks[0] % 10
    
    def draw_bet_pay(self):
        if self.player_hand.triple_three and self.player_hand.is_suited:
            # print('suited', self.player_hand)
            return 30.0
        if self.player_hand.triple_three:
            # print('unsuited', self.player_hand)
            return 9.0
        if self.player_hand.hand_value == 9:
            return 3.0
        if self.player_hand.hand_value == 8:
            return 2.0
        if self.player_hand.hand_value == 7:
            return 1.5
        else:
            return 1.0

    def winner_pay(self) -> None:
        return 1.0 * self.player_hand.enter_bet + self.draw_bet_pay() * self.player_hand.draw_bet

    def determine_winner(self):
        if self.player_hand.hand_value > self.banker_hand.hand_value:
            return self.winner_pay()
        if self.player_hand.hand_value == self.banker_hand.hand_value:
            return 0.0
        else:
            return -1.0 * (self.player_hand.enter_bet + self.player_hand.draw_bet)

    def player_draws(self):
        if self.player_hand.drawing_to_triple_three_suited:
            return True
        if self.player_hand.hand_value in [0, 1, 2]:
            return True
        if self.player_hand.hand_value in [3, 4] and self.banker_first_card_rank in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return True
        if self.player_hand.hand_value == 5 and self.banker_first_card_rank in [0, 1, 2, 3, 4, 5, 6, 7]:
            return True
        return False
    
    def banker_draws(self):
        return self.banker_hand.hand_value <= 4           

    def play(self) -> None:
        if self.player_draws():
            self.player_hand.draw_bet = self.player_hand.bet_unit
            self.player_hand.add_card(self.draw_card())

        if self.banker_draws():
            self.banker_hand.add_card(self.draw_card())

        self.player_hand.amount_won = self.determine_winner()


if __name__ == "__main__":

    num_hands = 50000000
    amount_bet = 0
    amount_won = 0
    
    data = []
    file_count = 1


    game = LuckyDrawBaccarat()

    print(game.player_hand)
    print(game.banker_first_card_rank)
    print(game.banker_hand)

    game.play()

    print(game.player_hand, ' ', game.player_hand.hand_value)
    print(game.banker_hand, ' ', game.banker_hand.hand_value)
    print(game.player_hand.amount_won, ' ', game.player_hand.draw_bet + game.player_hand.enter_bet )

    for iter in range(1, num_hands+1):
        game = LuckyDrawBaccarat()
        game.play()
    
        amount_bet_game = game.player_hand.draw_bet + game.player_hand.enter_bet
        amount_won_game = game.player_hand.amount_won

        amount_bet += amount_bet_game
        amount_won += amount_won_game
        
        if iter % 500000 == 0:
            print(iter, ' ', amount_bet, ' ', amount_won, ' ', amount_won/amount_bet, amount_won/iter)

    print(num_hands, ' ', amount_bet, ' ', amount_won, ' ', amount_won/amount_bet, amount_won/num_hands)
    