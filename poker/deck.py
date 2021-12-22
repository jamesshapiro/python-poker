import random
from collections import namedtuple

legible_ranks = {i: str(i) for i in range(2,11)}
face_cards = {i+11: 'JQKA'[i] for i in range(4)}
legible_ranks.update(face_cards)

class Card(namedtuple('Card', ['rank', 'suit'])):
    def __str__(self):
        return(''.join([legible_ranks[self.rank], self.suit]))

class Deck:
    def __init__(self):
        ranks = range(2,15)
        suits = ['♥', '♣', '♠', '♦']
        self.cards = [Card(rank, suit)
                      for rank in ranks
                      for suit in suits]
    def remove(self, card):
        self.cards.remove(card)
    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards
    def __getitem__(self, idx):
        return self.cards[idx]

