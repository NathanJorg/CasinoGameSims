from Cards import Deck

class Baccarat:
    def __init__(self, decks=8, no_commission=False):
        self.deck = Deck(decks)
        self.deck.shuffle()
        self.no_commission = no_commission

        self.player_hand = []
        self.banker_hand = []

        self.start_game()

    def start_game(self) -> None:
        self.player_hand.append(self.deck.draw_card())
        self.player_hand.append(self.deck.draw_card())
        self.banker_hand.append(self.deck.draw_card())
        self.banker_hand.append(self.deck.draw_card())
    
    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
    
    def hand_value(self, hand):
        return (sum(card.card_value() for card in hand) % 10)
    
    def winner_pay(self):
        # return: banker_win, player_win, tie_win
        player_value = self.hand_value(self.player_hand)
        banker_value = self.hand_value(self.banker_hand)
        if player_value == banker_value:
            return 1.0, 1.0, 9.0
        elif player_value > banker_value:
            return 0.0, 2.0, 0.0
        
        # banker win
        elif self.no_commission:
            if banker_value == 6:
                return 1.5, 0.0, 0.0
            else:
                return 2.0, 0.0, 0.0
        else:
            return 1.95, 0.0, 0.0
    
    def play(self) -> None:
        
        player_value = self.hand_value(self.player_hand)
        banker_value = self.hand_value(self.banker_hand)

        if player_value in [8, 9] or banker_value in [8, 9]:
            pass

        elif player_value in [6, 7] and banker_value <= 5:
            self.banker_hand.append(self.deck.draw_card())

        elif player_value <= 5:
            self.player_hand.append(self.deck.draw_card())

            card_three_value = self.player_hand[2].card_value() % 10

            if banker_value == 6 and card_three_value in [6, 7]:
                self.banker_hand.append(self.deck.draw_card())
            elif banker_value == 5 and card_three_value in [4, 5, 6, 7]:
                self.banker_hand.append(self.deck.draw_card())
            elif banker_value == 4 and card_three_value in [2, 3, 4, 5, 6, 7]:
                self.banker_hand.append(self.deck.draw_card())
            elif banker_value == 3 and card_three_value in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
                self.banker_hand.append(self.deck.draw_card())
            elif banker_value in [0, 1, 2]:
                self.banker_hand.append(self.deck.draw_card())
            else:
                pass

        