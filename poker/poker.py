#!/usr/bin/env python3 -tt

from deck import Deck
import itertools
import collections

StraightFlush = namedtuple('StraightFlush', ['highcard'])
FourOfAKind = namedtuple('FourOfAKind', ['four_rank', 'kicker'])
FullHouse = namedtuple('FullHouse', ['three_rank', 'two_rank'])
Flush = namedtuple('Flush', ['high', 'second', 'third', 'fourth', 'fifth'])
Straight = namedtuple('Straight', ['highcard'])
ThreeOfAKind = namedtuple('ThreeOfAKind', ['three_rank', 'kicker1', 'kicker2'])
TwoPair = namedtuple('TwoPair', ['high_pair', 'lower_pair', 'kicker'])
Pair = namedtuple('Pair', ['two_rank', 'kicker1', 'kicker2', 'kicker3'])
HighCard = namedtuple('HighCard', ['high', 'second', 'third', 'fourth', 'fifth'])

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.is_flush = False
        self.is_straight = False
        
        self.suit_count = collections.Counter()
        self.rank_count = collections.Counter()
        
        for card in hand:
            self.suit_count[card.suit] += 1
            self.rank_count[card.rank] += 1
            
        self.suit_counts = {*suit_count.values()}
        self.rank_counts = {*rank_count.values()}
        
        self.ranks = {*rank_count.keys()}
        if len(self.ranks) == 5:
            if max(self.ranks) - min(self.ranks) == 4 or {1, 10, 11, 12, 13} < self.ranks:
                self.is_straight = True
        self.is_flush = (max(self.suit_counts) == 5)
        if self.is_straight and self.is_flush:
            if max(self.ranks) - min(self.ranks) == 4:
                return StraightFlush(max(self.ranks))
            else:
                return StraightFlush(1)
        if self.rank_counts.most_common(1)[0][0] == 4:
            four, kicker = self.rank_count.most_common(2)
            return FourOfAKind(four, kicker)
        if self.rank_count.most_common(2)[0][0], self.rank_count.most_common(2)[1][0] == 3, 2:
            three, two = self.rank_count.most_common(2)
        if self.is_flush:
            self.ranks = sorted(list(ranks), reverse=True)
            return Flush(*self.ranks)
        if self.is_straight:
            if max(self.ranks) - min(self.ranks) == 4:
                return Straight(max(self.ranks))
            else:
                return Straight(1)
        if self.rank_counts.most_common(1)[0][0] == 3:
            
            

d = Deck()
d.shuffle()
player1 = []
player2 = []
firstFive = d[:5]
player1 = d[5:7] + d[:5]
player2 = d[7:9] + d[:5]

player1allhands = list(itertools.combinations(player1, 5))
hand = list(player1allhands[0])

#def evaluate_hand(hand):
suit_count = collections.Counter()
rank_count = collections.Counter()
for card in hand:
    suit_count[card.suit] += 1
    rank_count[card.rank] += 1
ranks = {*rank_count.keys()}
