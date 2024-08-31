from Cards import Card, SpanishDeck

from Blackjack import Blackjack
from BlackjackHand import BlackjackHand, SpBlackjackHand

from WriteToFile import WriteToFile as wtf

class SpBlackjack(Blackjack):
    def __init__(self, num_decks=6):
        super().__init__(num_decks=num_decks)
        self.deck = SpanishDeck(num_decks)
        self.deck.shuffle()

        self.player_hands = [SpBlackjackHand(self.draw_card(number_of_cards=2))]
        self.dealer_hand = BlackjackHand(self.draw_card(number_of_cards=2))

        self.hand_amount_wagered = 0.0
        self.hand_amount_won = 0.0

    def draw_card(self, number_of_cards=1):
        cards = [self.deck.draw_card() for _ in range(number_of_cards)]
        return cards if number_of_cards > 1 else cards[0]
    
    def dealer_play(self) -> None:
        while True:
            if self.dealer_hand.hand_value >= 18:
                break
            elif self.dealer_hand.hand_value == 17 and not self.dealer_hand.is_hand_soft:
                break
            else:
                self.dealer_hand.add_card(self.draw_card())

    def three_to_one_pay(self, hand: SpBlackjackHand):
        return (
            hand.seven_card_21 or
            (hand.six_seven_eight and hand.is_spades) or
            (hand.triple_seven and hand.is_spades)
        )

    def two_to_one_pay(self, hand: SpBlackjackHand):
        return (
            hand.six_card_21 or
            (hand.six_seven_eight and hand.is_suited) or
            (hand.triple_seven and hand.is_suited)
        )
    def three_to_two_pay(self, hand: SpBlackjackHand):
        return (
            hand.five_card_21 or
            hand.six_seven_eight or
            hand.triple_seven
        )

    def calculate_payout(self, hand: SpBlackjackHand):
        if hand.is_hand_busted:
            return -1.0
        elif hand.is_hand_blackjack:
            return self.blackjack_pay
        elif self.three_to_one_pay(hand):
            return 3.0
        elif self.two_to_one_pay(hand):
            return 2.0
        elif self.three_to_two_pay(hand):
            return 1.5
        elif self.player_wins(hand):
            return 1.0
        elif self.player_ties(hand):
            return 0.0
       
        # all other hands lose
        return -1.0
    
    def double_down_surrender(self, hand: SpBlackjackHand):
        if hand.hand_value in [12, 13, 14, 15, 16] and self.dealer_first_card_rank in [8, 9, 10, 11]:
            return True
        if hand.hand_value == 17 and self.dealer_first_card_rank == 11:
            return True
        return False
    
    def split_player_hand(self, hand: SpBlackjackHand) -> None:
        new_hand = SpBlackjackHand([hand.hand.pop()])
        hand.add_card(self.draw_card())
        new_hand.add_card(self.draw_card())
        hand.mark_split()
        new_hand.mark_split()
        self.player_hands.append(new_hand)
    
    def double_down(self, hand: SpBlackjackHand) -> None:
        hand.wagered_amount *= 2
        hand.add_card(self.draw_card())
        hand.mark_doubled()
    
    def does_player_split(self, hand: SpBlackjackHand):
        if not hand.can_split:
            return False
        
        card_rank = hand.card_ranks[0]

        if card_rank in [2, 3] and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8]:
            return True
        if card_rank == 6 and self.dealer_first_card_rank in [4, 5, 6]:
            return True  
        if card_rank == 7 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7]:
            return True if not (hand.is_suited or hand.is_spades) else False
        if card_rank == 8 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return True
        if card_rank == 9 and self.dealer_first_card_rank in [3, 4, 5, 6, 8, 9]:
            return True
        if card_rank == 11 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9, 10] and len(self.player_hands) == 1: # player cannot resplit aces
            return True
        
        return False
    
    def does_player_double(self, hand: SpBlackjackHand):
        if hand.is_hand_soft:
            if hand.hand_value == 15 and self.dealer_first_card_rank == 6 and len(hand.hand) < 4:
                return True
            elif hand.hand_value == 16:
                if self.dealer_first_card_rank == 5 and len(hand.hand) < 3:
                    return True
                if self.dealer_first_card_rank == 6 and len(hand.hand) < 4:
                    return True
            elif hand.hand_value == 17:
                if self.dealer_first_card_rank == 4 and len(hand.hand) < 3:
                    return True
                if self.dealer_first_card_rank == 5 and len(hand.hand) < 4:
                    return True  
                if self.dealer_first_card_rank == 6 and len(hand.hand) < 5:
                    return True
            elif hand.hand_value == 18:
                if self.dealer_first_card_rank == 4 and len(hand.hand) < 4:
                    return True
                if self.dealer_first_card_rank == 5 and len(hand.hand) < 5:
                    return True  
                if self.dealer_first_card_rank == 6 and len(hand.hand) < 6:
                    return True   
        else:
            if hand.hand_value == 9 and self.dealer_first_card_rank == 6 and len(hand.hand) < 4:
                return True
            elif hand.hand_value == 10:
                if self.dealer_first_card_rank in [4, 5, 6]:
                    return True
                if self.dealer_first_card_rank == 8 and len(hand.hand) < 3:
                    return True
                if self.dealer_first_card_rank == 7 and len(hand.hand) < 4:
                    return True
                if self.dealer_first_card_rank in [2, 3] and len(hand.hand) < 5:
                    return True
            elif hand.hand_value == 11:
                if self.dealer_first_card_rank in [2, 7, 8, 9] and len(hand.hand) < 4:
                    return True
                if self.dealer_first_card_rank in [3, 4, 5, 6] and len(hand.hand) < 5:
                    return True
        
        return False
    
    def does_player_stand(self, hand: SpBlackjackHand):
        if hand.has_split and hand.card_ranks[0] == 11: # player has split aces
            return True

        if hand.is_hand_soft:
            if hand.hand_value == 18:
                if self.dealer_first_card_rank in [2, 3, 4, 5, 6, 8] and len(hand.hand) < 4:
                    return True
                if self.dealer_first_card_rank == 7 and len(hand.hand) < 6:
                    return True
            elif hand.hand_value == 19:
                if self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7, 8, 9]:
                    return True
                if self.dealer_first_card_rank in [10, 11] and len(hand.hand) < 5:
                    return True
            elif hand.hand_value > 19:
                return True     
        else:
            if hand.hand_value == 13 and self.dealer_first_card_rank == 6:
                if hand.is_drawing_to_six_seven_eight:
                    return False
                if len(hand.hand) < 4:
                    return True
            elif hand.hand_value == 14 and self.dealer_first_card_rank == 4:
                if hand.is_drawing_to_six_seven_eight:
                    return False   
                if len(hand.hand) < 4:
                    return True        
            elif hand.hand_value == 14 and self.dealer_first_card_rank == 5:
                if hand.is_drawing_to_six_seven_eight and (hand.is_suited or hand.is_spades):
                    return False   
                if len(hand.hand) < 5:
                    return True        
            elif hand.hand_value == 14 and self.dealer_first_card_rank == 6:
                if hand.is_drawing_to_six_seven_eight and hand.is_spades:
                    return False   
                if len(hand.hand) < 5:
                    return True 
            elif hand.hand_value == 15 and self.dealer_first_card_rank == 2:
                if hand.is_drawing_to_six_seven_eight:
                    return False
                if len(hand.hand) < 4:
                    return True
            elif hand.hand_value == 15 and self.dealer_first_card_rank == 3:
                if hand.is_drawing_to_six_seven_eight and (hand.is_suited or hand.is_spades):
                    return False
                if len(hand.hand) < 5:
                    return True
            elif hand.hand_value == 15 and self.dealer_first_card_rank == 4 and len(hand.hand) < 5:
                return True
            elif hand.hand_value == 15 and self.dealer_first_card_rank in [5, 6] and len(hand.hand) < 6:
                return True
            elif hand.hand_value == 16 and self.dealer_first_card_rank == 2 and len(hand.hand) < 5:
                return True
            elif hand.hand_value == 16 and self.dealer_first_card_rank in [3, 4] and len(hand.hand) < 6:
                return True
            elif hand.hand_value == 16 and self.dealer_first_card_rank in [5, 6]:
                return True
            elif hand.hand_value == 17 and self.dealer_first_card_rank in [2, 3, 4, 5, 6, 7]:
                return True
            elif hand.hand_value == 17 and self.dealer_first_card_rank in [8, 9, 10] and len(hand.hand) < 6:
                return True
            elif hand.hand_value > 17:
                return True

        return False
    
    def optimal_strategy(self, hand: SpBlackjackHand) -> None:
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

    def is_hand_auto_resolved(self, hand: SpBlackjackHand):
        if hand.is_hand_blackjack:
            return True
        if self.three_to_one_pay(hand):
            return True
        if self.two_to_one_pay(hand):
            return True
        if self.three_to_two_pay(hand):
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

    def play(self):
        hand_index = 0
        while hand_index < len(self.player_hands):
            self.optimal_strategy(self.player_hands[hand_index])
            hand_index += 1

    # def win(self):
    #     for hand in self.player_hands:
    #         self.set_hand_winnings(hand) 
    #         if self.dealer_hand.is_hand_blackjack and not hand.is_hand_blackjack:
    #             hand.amount_won = -1.0      # dealer takes original bet only, any additional a=hands through splitting will be skipped
    #             break                   
    #         else:
    #             self.set_hand_winnings(hand)

    def set_hand_winnings(self, hand: SpBlackjackHand):
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
        game = SpBlackjack()
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

        if iter % 100000 == 0:
            print('Hand', iter, 'Current house edge: ', amount_won/iter)
            filename = f'.\\Spanish Blackjack Results\\results_{file_count}.txt'
            filename_csv = f'.\\Spanish Blackjack Results\\results_{file_count}.csv'
            wtf.write_to_file(data, filename, headers)
            wtf.write_to_csv(data, filename_csv, headers)
            file_count += 1
            data = []
            

    if data:
        filename = f'.\\Spanish Blackjack Results\\results_{file_count}.txt'
        wtf.write_to_file(data, filename, headers)  
        wtf.write_to_csv(data, filename_csv, headers) 

    print('Hand', num_hands, 'House edge: ', amount_won/num_hands)

