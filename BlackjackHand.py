from Cards import Card

class BlackjackHand:

    def __init__(self, hand: list[Card]=None) -> None: 
        self.hand = hand if hand else []
        self.wagered_amount = 1.0
        self.amount_won = 0.0
        self._has_doubled = False
        self._has_split = False
        self.update_hand_value()

    def __str__(self):
        hand_string = ", ".join(map(str, self.hand))
        return hand_string    
    
    def add_card(self, card) -> None:
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)

        self.update_hand_value()

    def update_hand_value(self) -> None:
        value = sum(card.card_value() for card in self.hand)

        num_aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        self._num_aces_left = num_aces
        self._hand_value = value

    def mark_doubled(self) -> None:
        self._has_doubled = True

    def mark_split(self) -> None:
        self._has_split = True
        
    @property
    def hand_value(self):
        return self._hand_value
    
    @property
    def is_hand_soft(self):
        return self._num_aces_left > 0
    
    @property 
    def is_hand_blackjack(self):
        return self._hand_value == 21 and len(self.hand) == 2 and not self.has_split
    
    @property
    def is_hand_busted(self):
        return self._hand_value > 21
    
    @property
    def card_ranks(self):
        return [card.card_value() for card in self.hand]

    @property
    def can_split(self):
        return len(self.hand) == 2 and self.card_ranks[0] == self.card_ranks[1]
    
    @property
    def has_doubled(self):
        return self._has_doubled

    @property
    def has_split(self):
        return self._has_split


class BlackjackChallengeHand(BlackjackHand):
    @property
    def is_five_card_charlie(self):
        return len(self.hand) == 5 and not self.is_hand_busted
    
    @property 
    def is_hand_blackjack(self):
        return self._hand_value == 21 and len(self.hand) == 2 

    @property
    def blackjack_rank(self):
        if not self.is_hand_blackjack:
            return None
        
        rank_values = {
            '10': 1, 'J': 2, 'Q': 3, 'K': 4
        }

        for card in self.hand:
            if card.rank in rank_values:
                return rank_values[card.rank]
            
        return None
    
class SpBlackjackHand(BlackjackHand):
    
    def __init__(self, hand: list[Card] = None) -> None: 
        super().__init__(hand)
        self._has_surrendered = False
        self.update_suits()

    def add_card(self, card) -> None:
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)

        self.update_hand_value()
        self.update_suits()

    def mark_surrendered(self) -> None:
        self._has_surrendered = True

    def update_suits(self):
        suits = [card.suit for card in self.hand]

        if len(set(suits)) == 1 and suits[0] == "\u2660": 
            self._spades = True
        elif len(set(suits)) == 1:
            self._suited = True
        else: 
            self._mixed = True

    @property
    def triple_seven(self):
        sevens_count = sum(1 for card in self.hand if card.rank == '7')
        return sevens_count and len(self.hand) == 3 and not self.has_doubled

    @property
    def six_seven_eight(self):
        required_ranks = {'6', '7', '8'}
        hand_ranks = {card.rank for card in self.hand}
        return hand_ranks == required_ranks and not self.has_doubled

    @property
    def five_card_21(self):
        return len(self.hand) == 5 and self.hand_value == 21 and not self.has_doubled
    
    @property
    def six_card_21(self):
        return len(self.hand) == 6 and self.hand_value == 21 and not self.has_doubled 
    
    @property
    def seven_card_21(self):
        return len(self.hand) >= 7 and self.hand_value == 21 and not self.has_doubled

    @property
    def is_spades(self):
        return self._spades
    
    @property
    def is_suited(self):
        return self._suited
    
    @property
    def is_mixed(self):
        return self._mixed

    @property
    def has_surrendered(self):
        return self._has_surrendered