from Cards import Card

class BaccaratHand:
    def __init__(self, hand: list[Card]=None) -> None: 
        self.hand = hand if hand else []
        self.bet_unit = 1.0
        self.enter_bet = self.bet_unit
        self.draw_bet = 0.0
        self.amount_won = 0.0
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
        value = sum(card.card_value() for card in self.hand) % 10
        self._hand_value = value

    @property
    def hand_value(self):
        return self._hand_value
    
    @property
    def card_ranks(self):
        return [card.card_value() % 10 for card in self.hand]
    
    @property
    def third_card_value(self):
        if len(self.card_ranks) == 3:
            return self.card_ranks[2]

class LuckyDrawHand(BaccaratHand):
    def __init__(self, hand: list[Card] = None) -> None:
        super().__init__(hand)
        self.update_suits()

    def add_card(self, card) -> None:
        if isinstance(card, list):
            self.hand.extend(card)
        else:
            self.hand.append(card)

        self.update_hand_value()
        self.update_suits()

    def update_suits(self) -> None:
        suits = [card.suit for card in self.hand]
        self._is_suited = True if len(set(suits)) == 1 else False
            
    @property
    def is_suited(self):
        return self._is_suited
    
    @property
    def is_triple_three(self):
        return self._is_suited
    
    @property
    def triple_three(self):
        threes_count = sum(1 for card in self.hand if card.rank == '3')
        return threes_count == 3 and len(self.hand) == 3
    
    @property
    def drawing_to_triple_three(self):
        return len(self.card_ranks) == 2 and self.card_ranks == [3, 3]
    
    @property
    def drawing_to_triple_three_suited(self):
        return len(self.card_ranks) == 2 and self.card_ranks == [3, 3] and self.is_suited
