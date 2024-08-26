from Cards import SpanishDeck

class SpanishBlackjack():

    def __init__(self, num_decks=6, bet=1.0, blackjack_pay = 3/2, max_hands=2, double_after_split=True):
        self.deck = SpanishDeck(num_decks)
        self.deck.shuffle()
        self.bet = bet
        
        # game attributes
        self.max_hands = max_hands
        self.blackjack_pay = blackjack_pay
        self.double_after_split = double_after_split

        #game initialisation
        self.player_hands = [[]]
        self.dealer_hand = []
        self.player_bet = []
        self.amount_won = 0.0
        self.start_game()     

    def start_game(self):
        self.player_bet.append(self.bet)
        self.player_hands[0].append(self.deck.draw_card())
        self.player_hands[0].append(self.deck.draw_card())
        self.dealer_hand.append(self.deck.draw_card())

    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str

    def hand_value(self, hand, has_doubled=False):

        value = sum(card.card_value(has_doubled) for card in hand) 

        if not has_doubled:
            num_aces = sum(1 for card in hand if card.rank == 'A')        
            while value > 21 and num_aces:
                value -= 10
                num_aces -= 1

        return value, num_aces > 0

    def hit(self, hand):
        hand.append(self.deck.draw_card())
      
    def check_blackjack(self, hand):
        return (self.hand_value(hand)[0] == 21 and len(hand) == 2)

    def player_hit(self, hand_index=0):
        self.player_hands[hand_index].append(self.deck.draw_card())

    def double_down(self, hand_index):
        self.player_bet[hand_index] += self.bet
        self.player_hit(hand_index)

    def dealer_play(self):

        while True:
            dealer_value, is_soft = self.hand_value(self.dealer_hand)
            if dealer_value >= 18:
                break
            elif dealer_value == 17 and not is_soft:
                break
            else:
                self.dealer_hand.append(self.deck.draw_card())

    def can_split(self, hand):
        return len(hand) == 2 and hand[0].rank == hand[1].rank

    def check_for_splits(self, hand_index, dealer_card):
        hand = self.player_hands[hand_index]
        if not self.can_split(hand):
            return False
        
        player_rank = hand[0].rank
        
        if player_rank in ['2' ,'3'] and dealer_card in [2, 3, 4, 5, 6, 7, 8]:
            return True
        elif player_rank == '6' and dealer_card in [4, 5, 6]:
            return True
        elif player_rank == '7' and dealer_card in [2, 3, 4, 5, 6, 7]:
            return False if hand[0].suit == hand[1].suit else True
        elif player_rank in ['8', 'A']:
            return True
        elif player_rank == '9' and dealer_card in [3, 4, 5, 6, 8, 9]:
            return True
        else:
            return False
        
        
    def split_hand(self, hand_index):
        hand = self.player_hands[hand_index]
        new_hand = [hand.pop()]
        self.player_hands.append(new_hand)
        
    def determine_winner(self):
        dealer_value, _ = self.hand_value(self.dealer_hand)

        for hand_index, hand in enumerate(self.player_hands):
            player_value, _ = self.hand_value(hand)       

            if self.check_blackjack(self.dealer_hand):
     
                if self.check_blackjack(hand) and len(self.player_hands) == 1: # check if player also has blackjack
                    self.amount_won += self.player_bet[0]
                else:
                    # dealer takes original bet only
                    self.player_bet = [self.bet]
            
            elif self.check_blackjack(hand) and len(self.player_hands) == 1:
                self.amount_won += self.player_bet[0] + self.player_bet[0] * self.blackjack_pay
            elif player_value > 21:
                continue 
            elif dealer_value > 21:
                self.amount_won += 2 * self.player_bet[hand_index]
            elif player_value > dealer_value:
                self.amount_won += 2 * self.player_bet[hand_index]
            elif player_value < dealer_value:
                continue 
            else:
                self.amount_won += self.player_bet[hand_index]

    def optimal_strategy(self):
        hand_index = 0
        dealer_value = self.dealer_hand[0].card_value()
       
        while hand_index < len(self.player_hands):
            hand = self.player_hands[hand_index]
            while True:
                               
                # check for splits
                if self.check_for_splits(hand_index, dealer_value) and len(self.player_hands) < self.max_hands:
                    self.split_hand(hand_index)
                    self.player_bet.append(self.bet)

                # player has split aces and gets one card only
                if len(self.player_hands[hand_index]) == 1 and self.player_hands[hand_index][0].rank == 'A':
                    self.player_hit(hand_index)
                    break

                player_value, is_soft = self.hand_value(hand)

                # player stands
                if player_value >= 19 and is_soft:
                    break
                elif player_value == 18 and dealer_value in [2, 3, 4, 5, 6, 7, 8] and is_soft:
                    break
                elif player_value >= 17 and not is_soft:
                    break
                elif player_value in [13, 14, 15, 16] and dealer_value in [2, 3, 4, 5, 6] and not is_soft:
                    break
                elif player_value == 12 and dealer_value in [4, 5, 6] and not is_soft:
                    break
                                
                # player doubles
                elif self.double_after_split or len(self.player_hands) == 1:    # check if player has one hand only if doubling after split is not allowed

                    if player_value == 9 and dealer_value == 9:
                        self.double_down(hand_index) if len(self.player_hands[hand_index]) < 4 else None
                        break
                    elif player_value == 10 and dealer_value:
                        self.double_down(hand_index)
                        break
                    elif player_value == 11:
                        self.double_down(hand_index)
                        break    
                    else:    
                        self.player_hit(hand_index)       
               
                # draw card
                else:
                    self.player_hit(hand_index)

            hand_index += 1

    def play(self):
        self.optimal_strategy()
        self.dealer_play()
        self.determine_winner()  



game = SpanishBlackjack()

game.play()

print(game.print_hand(game.player_hands[0]))
print(game.hand_value(game.player_hands[0])[0])


# print(deck.count())

# deck.shuffle()

# print(deck)

# card = deck.draw_card()

# print(card.card_value())

# print(deck.count())