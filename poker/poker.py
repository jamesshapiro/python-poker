#!/usr/bin/env python3 -tt

from deck import Deck
from deck import Card
import itertools
from collections import namedtuple
import collections
from functools import total_ordering

@total_ordering
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.is_flush = False
        self.is_straight = False
        self.value = []
        self.suit_count = collections.Counter()
        self.rank_count = collections.Counter()
        for card in self.cards:
            self.suit_count[card.suit] += 1
            self.rank_count[card.rank] += 1

        self.suit_counts = {*self.suit_count.values()}
        self.rank_counts = {*self.rank_count.values()}
        self.ranks = {*self.rank_count.keys()}
        if len(self.ranks) == 5:
            if max(self.ranks) - min(self.ranks) == 4 or {14, 2, 3, 4, 5} < self.ranks:
                self.is_straight = True
        self.lst = sorted(self.cards, key=lambda crd: crd.rank, reverse=True)
        self.lst = sorted(self.lst, key=lambda crd: self.rank_count[crd.rank], reverse=True)
        self.lst = list(map(lambda crd: crd.rank, self.lst))
        if {14, 2, 3, 4, 5} < self.ranks:
            self.lst = self.lst[1:] + self.lst[0:1]
        self.is_flush = max(self.suit_counts) == 5
        if self.is_straight and self.is_flush:
            self.value = [9] + self.lst
        elif max(self.rank_counts) == 4:
            self.value = [8] + self.lst
        elif (self.rank_count.most_common(2)[0][1], self.rank_count.most_common(2)[1][1]) == (3, 2):
            self.value = [7] + self.lst
        elif self.is_flush:
            self.value = [6] + self.lst
        elif self.is_straight:
            self.value = [5] + self.lst
        elif max(self.rank_counts) == 3:
            self.value = [4] + self.lst
        elif (self.rank_count.most_common(2)[0][1], self.rank_count.most_common(2)[1][1]) == (2, 2):
            self.value = [3] + self.lst
        elif max(self.rank_counts) == 2:
            self.value = [2] + self.lst
        else:
            self.value = [1] + self.lst

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

d = Deck()
d.shuffle()
player1 = []
player2 = []
firstFive = d[:5]
player1 = d[5:7] + d[:5]
player2 = d[7:9] + d[:5]

player1allhands = list(itertools.combinations(player1, 5))
player2allhands = list(itertools.combinations(player2, 5))
combos = list(player1allhands)
bestComboForP1 = max(combos, key=lambda x: Hand(x).value)
combos = list(player2allhands)
bestComboForP2 = max(combos, key=lambda x: Hand(x).value)
if Hand(bestComboForP1) > Hand(bestComboForP2):
    print("Player 1 wins!:")

elif Hand(bestComboForP1) < Hand(bestComboForP2):
    print("Player 2 wins!:")
    print("P1: {}".format(Hand(bestComboForP1).value))
    print("P2: {}".format(Hand(bestComboForP2).value))
else:
    print("It's a tie!:")
print("P1 pocket: {}".format(player1[0:2]))
print("P2 pocket: {}".format(player2[0:2]))
print("Table cards: {}".format(player1[2:]))
print("P1: {}".format(Hand(bestComboForP1).value))
print("P2: {}".format(Hand(bestComboForP2).value))

hand = Hand([Card(rank=12, suit='clubs'), Card(rank=13, suit='hearts'), Card(rank=12, suit='spades'), Card(rank=3, suit='diamonds'), Card(rank=3, suit='spades')])
