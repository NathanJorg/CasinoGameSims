import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit

    def card_value(self, has_player_doubled=False):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 1 if has_player_doubled else 11     # In Spansish Blackjack, an Ace always counts as 1 after doubling
        else:
            return int(self.rank)
    

class Deck():
    club = "\u2663"
    heart = "\u2665"
    diamond = "\u2666"
    spade = "\u2660"

    suits = [club, heart, diamond, spade] 
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] 

    def __init__(self, num_decks=1):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks for _ in range(num_decks)]

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None
    
    def count(self):
        return len(self.cards)
    
    
class SpanishDeck(Deck):
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K'] 
    