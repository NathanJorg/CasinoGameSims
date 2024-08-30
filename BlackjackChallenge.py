from Cards import Deck
from BlackjackHand import BlackjackChallengeHand
from WriteToFile import WriteToFile as wtf

import logging

class BlackjackChallenge():

    def __init__(self, num_decks=8, max_hands=3) -> None: 
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        
        self.max_hands = max_hands

        self.player_hands = [BlackjackChallengeHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackChallengeHand(self.draw_card(number_of_cards=2))

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
      
    @property
    def dealer_first_card_rank(self):
        return self.dealer_hand.card_ranks[0]
    
    def blackjack_pays(self, hand: BlackjackChallengeHand):
        if not self.dealer_hand.is_hand_blackjack:
            return 2.0
        if hand.blackjack_rank < self.dealer_hand.blackjack_rank:
            return 3.0
        if hand.blackjack_rank == self.dealer_hand.blackjack_rank:
            return 4.0
        if hand.blackjack_rank > self.dealer_hand.blackjack_rank:
            return 5.0 
 
    def calculate_payout(self, hand: BlackjackChallengeHand):
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

    def does_player_split(self, hand: BlackjackChallengeHand):
        if not hand.can_split:
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
    
    def does_player_double(self, hand: BlackjackChallengeHand):
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
    
    def does_player_stand(self, hand: BlackjackChallengeHand):
        if len(hand.hand) == 2 and hand.is_hand_soft:
            if hand.hand_value == 18 and self.dealer_first_card_rank in [7, 8]:
                return True
            if hand.hand_value > 18:
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
            if hand.hand_value > 17:
                return True
        
        if len(hand.hand) == 3 and hand.is_hand_soft:
            if hand.hand_value == 19 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8]:
                return True
            if hand.hand_value > 19:
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
            if hand.hand_value > 17:
                return True
            
        if len(hand.hand) == 4 and hand.is_hand_soft:
            if hand.hand_value == 21:
                return True
        if len(hand.hand) == 4 and not hand.is_hand_soft:
            if hand.hand_value == 16 and self.dealer_first_card_rank in [4, 5, 6]:
                return True
            if hand.hand_value == 17 and self.dealer_first_card_rank in [2, 3, 4, 5, 6]:
                return True
            if hand.hand_value > 17:
                return True
        
        if len(hand.hand) == 5:
            return True
        
        return False
            
    def split_player_hand(self, hand: BlackjackChallengeHand) -> None:
        new_hand = BlackjackChallengeHand([hand.hand.pop()])
        hand.add_card(self.draw_card())
        new_hand.add_card(self.draw_card())
        self.player_hands.append(new_hand)
    
    def double_down(self, hand: BlackjackChallengeHand):
        hand.wagered_amount *= 2
        hand.mark_doubled()
        hand.add_card(self.draw_card())
    
    def optimal_strategy(self, hand: BlackjackChallengeHand):
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
        
    def is_hand_auto_resolved(self, hand: BlackjackChallengeHand):
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
        return sum(hand.wagered_amount for hand in self.player_hands if not self.is_hand_auto_resolved(hand)) > 0

    def win(self):
        unresolved_amount = self.amount_not_auto_resolved()

        for hand in self.player_hands:
            if self.is_hand_auto_resolved(hand):
                self.set_hand_winnings(hand)
            elif self.dealer_hand.is_hand_blackjack: 
                if unresolved_amount:
                    hand.amount_won = -1.0
                    unresolved_amount = False 
            else:
                self.set_hand_winnings(hand)

    def set_hand_winnings(self, hand: BlackjackChallengeHand):
        hand.amount_won = hand.wagered_amount * self.calculate_payout(hand)

    # def handle_blackjack_unresolved(self, hand: BlackjackChallengeHand, unresolved_amount):

    #     if unresolved_amount > hand.wagered_amount:
    #         unresolved_amount -= hand.wagered_amount
    #     else:
    #         if hand.has_doubled:
    #             hand.wagered_amount = 1.0
    #         self.set_hand_winnings(hand)

    #     return unresolved_amount

if __name__ == "__main__":

    num_hands = 10000000
    amount_bet = 0
    amount_won = 0

    player_header = []

    for hand in range(3):
        player_header.append('Hand_%s' % str(hand+1))
        player_header.append('Hand_value_%s' % str(hand+1))

    headers = ['Hand'] + player_header + ['Dealer_hand'] + ['Dealer_value'] + ['Bet_amount'] + ['Win_amount'] + ['Has_doubled']   

    data = []
    file_count = 1

    for iter in range(1, num_hands+1):
        game = BlackjackChallenge()
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
            elif game.player_hands[i].is_five_card_charlie:
                new_row['Hand_value_%s' % str(i+1)] = '5CC'
            else:
                new_row['Hand_value_%s' % str(i+1)] = game.player_hands[i].hand_value
    
        data.append(new_row)

        amount_bet += sum(hand.wagered_amount for hand in game.player_hands)
        amount_won += sum(hand.amount_won for hand in game.player_hands)

        if iter % 100000 == 0:
            print('Hand', iter, 'Current house edge: ', amount_won/iter)
            filename = f'.\\Blackjack Challenge Results\\results_bb1_{file_count}.txt'
            filename_csv = f'.\\Blackjack Challenge Results\\results_bb1_{file_count}.csv'
            wtf.write_to_file(data, filename, headers)
            wtf.write_to_csv(data, filename_csv, headers)
            file_count += 1
            data = []
            

    if data:
        filename = f'.\\Blackjack Challenge Results\\results_bb1_{file_count}.txt'
        wtf.write_to_file(data, filename, headers)  
        wtf.write_to_csv(data, filename_csv, headers) 

    print('Hand', num_hands, 'House edge: ', amount_won/num_hands)