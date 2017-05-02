#!/usr/bin/env python3 -tt

import random
from collections import namedtuple

legible_ranks = {}
for i in range(2,11):
    legible_ranks[i] = str(i)
legible_ranks[11] = 'J'
legible_ranks[12] = 'Q'
legible_ranks[13] = 'K'
legible_ranks[14] = 'A'

class Card(namedtuple('Card', ['rank', 'suit'])):
    def __str__(self):
        return(''.join([legible_ranks[self.rank], self.suit]))

class Deck:
    def __init__(self):
        suits = ['♥', '♣', '♠', '♦']
        ranks = range(13)
        self.cards = [Card(rank+2, suit)
                      for rank in ranks
                      for suit in suits]
    def remove(self, card):
        self.cards.remove(card)
    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards
    def __getitem__(self, idx):
        return self.cards[idx]

