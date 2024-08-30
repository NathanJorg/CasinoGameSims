from Cards import Deck
from BlackjackHand import BlackjackHand

from WriteToFile import WriteToFile as wtf

class Blackjack():
    def __init__(self, num_decks=6, blackjack_pay = 3/2, max_hands=2, hit_on_soft_17=False):
        self.deck = Deck(num_decks)
        self.deck.shuffle()

        self.blackjack_pay = blackjack_pay
        self.max_hands = max_hands
        self.hit_on_soft_17=hit_on_soft_17

        self.player_hands = [BlackjackHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackHand(self.draw_card(number_of_cards=2))

        self.hand_amount_wagered = 0.0
        self.hand_amount_won = 0.0

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    @property
    def dealer_first_card_rank(self):
        return self.dealer_hand.card_ranks[0]
    
    def calculate_payout(self, hand: BlackjackHand):
        if hand.is_hand_busted:
            return -1.0
        elif hand.is_hand_blackjack:
            return self.blackjack_pay if not self.dealer_hand.is_hand_blackjack else 0.0
        elif self.player_wins(hand):
            return 1.0
        elif self.player_ties(hand):
            return 0.0
       
        # all other hands lose
        return -1.0
    
    def player_wins(self, hand: BlackjackHand):
        if hand.is_hand_busted:
            return False
        elif self.dealer_hand.is_hand_busted:
            return True
        elif hand.hand_value > self.dealer_hand.hand_value:
            return True     

        return False

    def player_ties(self, hand:BlackjackHand):
        return hand.hand_value == self.dealer_hand.hand_value
    
    def dealer_play(self) -> None:
        while True:
            if self.dealer_hand.hand_value >= 18:
                break
            elif self.dealer_hand.hand_value == 17 and not self.hit_on_soft_17:
                break
            elif self.dealer_hand.hand_value == 17 and not self.dealer_hand.is_hand_soft:
                break
            else:
                self.dealer_hand.add_card(self.draw_card())

    def does_player_split(self, hand: BlackjackHand):
        if not hand.can_split:
            return False
        
        card_rank = hand.card_ranks[0]

        if card_rank in [2, 3] and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
            return True
        if card_rank == 4 and self.dealer_first_card_rank in [5, 6]:
            return True
        if card_rank == 6 and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
            return True  
        if card_rank == 7 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7]:
            return True
        if card_rank == 8:
            return True
        if card_rank == 9 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 8, 9]:
            return True
        if card_rank == 11 and len(self.player_hands) == 1: # player cannot resplit aces
            return True
        
        return False
    
    def does_player_double(self, hand: BlackjackHand):
        if len(hand.hand) != 2:
            return False
        if hand.hand_value == 9 and self.dealer_first_card_rank in [3, 4, 5, 6]:
            return True
        if hand.hand_value == 10 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        if hand.hand_value == 11 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return True
        return False
    
    def does_player_stand(self, hand: BlackjackHand):
        if hand.has_split and hand.card_ranks[0] == 11: # player has split aces
            return True

        if hand.is_hand_soft:
            if hand.hand_value > 18:
                return True
            elif hand.hand_value == 18 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8]:
                return True
            else:
                return False
        else:
            if hand.hand_value == 12 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            elif hand.hand_value in [13, 14, 15, 16] and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True
            elif hand.hand_value > 16:
                return True
            else:
                return False
            
    def split_player_hand(self, hand: BlackjackHand) -> None:
        new_hand = BlackjackHand([hand.hand.pop()])
        hand.add_card(self.draw_card())
        new_hand.add_card(self.draw_card())
        hand.mark_split()
        new_hand.mark_split()
        self.player_hands.append(new_hand)
    
    def double_down(self, hand: BlackjackHand) -> None:
        hand.wagered_amount *= 2
        hand.mark_doubled()
        hand.add_card(self.draw_card())

    def optimal_strategy(self, hand: BlackjackHand) -> None:
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

    def win(self):
        for hand in self.player_hands:
            if self.dealer_hand.is_hand_blackjack and not hand.is_hand_blackjack:
                hand.amount_won = -1.0      # dealer takes original bet only, any additional a=hands through splitting will be skipped
                break                   
            else:
                self.set_hand_winnings(hand)

    def set_hand_winnings(self, hand: BlackjackHand):
        hand.amount_won = hand.wagered_amount * self.calculate_payout(hand)

if __name__ == "__main__":

    num_hands = 10000000
    amount_bet = 0
    amount_won = 0

    player_header = []

    for hand in range(2):
        player_header.append('Hand_%s' % str(hand+1))
        player_header.append('Hand_value_%s' % str(hand+1))

    headers = ['Hand'] + player_header + ['Dealer_hand'] + ['Dealer_value'] + ['Bet_amount'] + ['Win_amount'] + ['Has_doubled']   

    data = []
    file_count = 1

    for iter in range(1, num_hands+1):
        game = Blackjack()
        game.play()
        game.dealer_play()
        game.win()

        if game.dealer_hand.is_hand_blackjack:
            dealer_value = 'BLACKJACK'
        elif game.dealer_hand.is_hand_busted:
            dealer_value = 'BUST'
        else:
            dealer_value = game.dealer_hand.hand_value

        new_row = {
            'Hand': iter,
            'Dealer_hand': game.dealer_hand,
            'Dealer_value': dealer_value,
            'Bet_amount': sum(hand.wagered_amount for hand in game.player_hands),
            'Win_amount': sum(hand.amount_won for hand in game.player_hands),
            'Has_doubled': any(hand.has_doubled for hand in game.player_hands)
        }

        for i in range(len(game.player_hands)):
            new_row['Hand_%s' % str(i+1)] = game.player_hands[i]
            if game.player_hands[i].is_hand_blackjack:
                new_row['Hand_value_%s' % str(i+1)] = 'BLACKJACK'
            elif game.player_hands[i].is_hand_busted:
                new_row['Hand_value_%s' % str(i+1)] = 'BUST'
            else:
                new_row['Hand_value_%s' % str(i+1)] = game.player_hands[i].hand_value
    
        data.append(new_row)

        amount_bet += sum(hand.wagered_amount for hand in game.player_hands)
        amount_won += sum(hand.amount_won for hand in game.player_hands)

        if iter % 200000 == 0:
            print('Hand', iter, 'Current house edge: ', amount_won/iter)
            filename = f'.\\Blackjack Results\\results_bb1_{file_count}.txt'
            filename_csv = f'.\\Blackjack Results\\results_bb1_{file_count}.csv'
            wtf.write_to_file(data, filename, headers)
            wtf.write_to_csv(data, filename_csv, headers)
            file_count += 1
            data = []
            

    if data:
        filename = f'.\\Blackjack Results\\results_bb1_{file_count}.txt'
        wtf.write_to_file(data, filename, headers)  
        wtf.write_to_csv(data, filename_csv, headers) 

    print('Hand', num_hands, 'House edge: ', amount_won/num_hands)