#!/usr/bin/env python3 -tt

import random
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class Deck:
    def __init__(self):
        self.suits = ['hearts', 'clubs', 'spades', 'diamonds']
        self.ranks = range(13)
        self.cards = [Card(rank+2, suit)
                      for rank in self.ranks
                      for suit in self.suits]
    def remove(self, card):
        self.cards.remove(card)
    def shuffle(self):
        random.shuffle(self.cards)
        return self.cards
    def __getitem__(self, idx):
        return self.cards[idx]

