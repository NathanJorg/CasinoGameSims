from Cards import Card


class BlackjackHand:
    def __init__(self, hand: list[Card]=None) -> None: 
        self.hand = hand if hand else []
        self.update_hand_value()

    def __str__(self):
        hand_string = ", ".join(map(str, self.hand))
        return hand_string    
    
    def add_card(self, card):
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)

        self.update_hand_value()

    def update_hand_value(self):
        value = sum(card.card_value() for card in self.hand)

        num_aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        self._num_aces_left = num_aces
        self._hand_value = value
        
    @property
    def hand_value(self):
        return self._hand_value
    
    @property
    def is_hand_soft(self):
        return self._num_aces_left > 0
    
    @property 
    def is_hand_blackjack(self):
        return self._hand_value == 21 and len(self.hand) == 2
    
    @property
    def card_ranks(self):
        return [card.card_value() for card in self.hand]

    def can_split(self):
        return len(self.hand) == 2 and self.card_ranks[0] == self.card_ranks[1]