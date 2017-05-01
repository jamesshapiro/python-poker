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
        self.distinct_ranks = {*self.rank_count.keys()}
        if len(self.distinct_ranks) == 5:
            if max(self.distinct_ranks) - min(self.distinct_ranks) == 4:
                self.is_straight = True
            elif {14, 2, 3, 4, 5} < self.distinct_ranks:
                self.is_straight = True
        self.lst = sorted(self.cards,
                          key=lambda crd: crd.rank,
                          reverse=True)
        self.lst = sorted(self.lst,
                          key=lambda crd: self.rank_count[crd.rank],
                          reverse=True)
        self.lst = list(map(lambda crd: crd.rank, self.lst))
        if {14, 2, 3, 4, 5} < self.distinct_ranks:
            self.lst = self.lst[1:] + self.lst[0:1]
        self.is_flush = max(self.suit_counts) == 5
        if self.is_straight and self.is_flush:
            self.value = [9] + self.lst
        elif max(self.rank_counts) == 4:
            self.value = [8] + self.lst
        elif (self.rank_count.most_common(2)[0][1],
              self.rank_count.most_common(2)[1][1]) == (3, 2):
            self.value = [7] + self.lst
        elif self.is_flush:
            self.value = [6] + self.lst
        elif self.is_straight:
            self.value = [5] + self.lst
        elif max(self.rank_counts) == 3:
            self.value = [4] + self.lst
        elif (self.rank_count.most_common(2)[0][1],
              self.rank_count.most_common(2)[1][1]) == (2, 2):
            self.value = [3] + self.lst
        elif max(self.rank_counts) == 2:
            self.value = [2] + self.lst
        else:
            self.value = [1] + self.lst

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

def evaluate_pocket_heads_up(card1,
                             card2,
                             n_other_players = 1,
                             num_simulations = 250):
    assert(n_other_players > 0)
    deck = Deck()
    deck.remove(card1)
    deck.remove(card2)
    player1 = [card1, card2]
    simulation_tally = [0, 0, 0]
    for _ in range(num_simulations):
        deck.shuffle()
        player1 += deck[:5]
        player1allhands = list(itertools.combinations(player1, 5))
        combos = list(player1allhands)
        bestComboForP1 = max(combos, key=lambda x: Hand(x).value)
        is_losing_hand = False
        is_tying_hand = False
        for i in range(n_other_players):
            other_player_i = deck[:5] + deck[5+(2*i):7+(2*i)]
            allhands = list(itertools.combinations(other_player_i, 5))
            combos = list(allhands)
            bestCombo = max(combos, key=lambda x: Hand(x).value)
            if Hand(bestComboForP1) < Hand(bestCombo):
                is_losing_hand = True
            elif Hand(bestComboForP1) == Hand(bestCombo):
                is_tying_hand = True
        if is_losing_hand:
            simulation_tally[1] += 1
        elif is_tying_hand:
            simulation_tally[2] += 1
        else:
            simulation_tally[0] += 1
        player1 = player1[:2]
    return [round(x/num_simulations, 4) for x in simulation_tally]
    
d = Deck()
d.shuffle()
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

pocket_aces = [Card(rank=14, suit='spades'), Card(rank=14, suit='clubs')]
sim = evaluate_pocket_heads_up(*pocket_aces, 3, 250)
print("Wins: {}, Losses: {}, Ties: {}".format(sim[0], sim[1], sim[2]))
