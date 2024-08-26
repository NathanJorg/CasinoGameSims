from Cards import Deck

from itertools import combinations
from collections import Counter

class PokerHand:
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    hand_rankings = {
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }

    def __init__(self, hand) -> None:
        self.hand = hand

    def __str__(self):
        _hand_string = ", ".join(map(str, self.hand))
        return _hand_string
    
    @property
    def ranks(self):
        sorted_list = sorted([self.rank_values[card.rank] for card in self.hand], reverse=True)

        frequency = Counter(sorted_list)

        result = sorted(sorted_list, key=lambda x: (-frequency[x], -x))

        # Handle the low-Ace straight case
        if result == [14, 5, 4, 3, 2]:
            result = [5, 4, 3, 2, 1]  # Treat Ace as '1'    
        
        return result
    
    @property
    def suits(self):
        suits = [card.suit for card in self.hand]
        return suits

    @property
    def hand_rank_value(self):
        return self.hand_rankings[self.evaluate_hand()]
    
    @property
    def hand_rank(self):
        return self.evaluate_hand()
    
    def is_royal_flush(self):
        return self.is_straight_flush() and self.ranks == [14, 13, 12, 11, 10]

    def is_straight_flush(self):
        return self.is_flush() and self.is_straight()

    def is_four_of_a_kind(self):
        return 4 in Counter(self.ranks).values()

    def is_full_house(self):
        rank_counts = Counter(self.ranks).values()
        return 3 in rank_counts and 2 in rank_counts

    def is_flush(self):
        return len(set(self.suits)) == 1

    def is_straight(self):
        return self.ranks == list(range(self.ranks[0], self.ranks[0] - 5, -1))

    def is_three_of_a_kind(self):
        return 3 in Counter(self.ranks).values()

    def is_two_pair(self):
        return len([count for count in Counter(self.ranks).values() if count == 2]) == 2

    def is_one_pair(self):
        return 2 in Counter(self.ranks).values()

    def evaluate_hand(self):
        if self.is_royal_flush():
            return "Royal Flush"
        elif self.is_straight_flush():
            return "Straight Flush"
        elif self.is_four_of_a_kind():
            return "Four of a Kind"
        elif self.is_full_house():
            return "Full House"
        elif self.is_flush():
            return "Flush"
        elif self.is_straight():
            return "Straight"
        elif self.is_three_of_a_kind():
            return "Three of a Kind"
        elif self.is_two_pair():
            return "Two Pair"
        elif self.is_one_pair():
            return "One Pair"
        else:
            return "High Card"
    
    def print_hand(self, hand):
        hand_str = ", ".join(map(str, hand))
        return hand_str
    
    def find_best_hand(self):
        _best_hand = None
        _best_rank_value = 0

        for combo in combinations(self.hand, 5):
            _current_hand = PokerHand(list(combo))
            if _current_hand.hand_rank_value > _best_rank_value:
                _best_hand = _current_hand
                _best_rank_value = _current_hand.hand_rank_value
            elif _current_hand.hand_rank_value == _best_rank_value:
                if _current_hand.ranks > _best_hand.ranks:
                    _best_hand = _current_hand

        return _best_hand
    
class PokerGame:
    def __init__(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = PokerHand(self.draw_cards(number_of_cards=7))
        self.dealer_hand = PokerHand(self.draw_cards(number_of_cards=7))

    def draw_cards(self, number_of_cards):
        return [self.deck.draw_card() for _ in range(number_of_cards)]


if __name__ == "__main__":

    count=1
    while True:
        game = PokerGame()
        best_hand = game.player_hand.find_best_hand()

        if best_hand.hand_rank == "One Pair":
            print(best_hand)
            print(game.player_hand.ranks)
            print(count)
            break
        count += 1

    #print(game.player_hand.sorted_ranks)
