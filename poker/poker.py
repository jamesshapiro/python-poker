from deck import Deck
from deck import Card
import itertools
from collections import namedtuple
import collections
from functools import total_ordering

NUM_SIMULATIONS = 2500
STRAIGHT_FLUSH = 9
FOUR_OF_A_KIND = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1

@total_ordering
class Hand:
    def __init__(self, cards):
        self.cards = cards
        is_flush = False
        is_straight = False
        self.value = []
        suit_count = collections.Counter()
        rank_count = collections.Counter()
        for card in self.cards:
            suit_count[card.suit] += 1
            rank_count[card.rank] += 1
        distinct_ranks = {card.rank for card in self.cards}
        ''' 
        'rank_count_shape' is an important criterion in assigning the hand
        to a 'category' (i.e. the category of 'Full House'). The other
        criteria are whether the hand is a straight or a flush (or
        both).
        
        Category        -> rank_count_shape
        ===============    =================
        Four-of-a-Kind  -> (4, 1)
        Full House      -> (3, 2)
        Three-of-a-Kind -> (3, 1, 1)
        Two Pair        -> (2, 2, 1)
        Pair            -> (2, 1, 1, 1)
        High Card       -> (1, 1, 1, 1, 1)
'''
        rank_count_shape = tuple(sorted(rank_count.values(), reverse=True))
        if rank_count_shape == (1, 1, 1, 1, 1):
            if max(distinct_ranks) - min(distinct_ranks) == 4:
                is_straight = True
            elif {14, 2, 3, 4, 5} < distinct_ranks:
                is_straight = True
        
        ''' The hand value is mapped to a list of integers
        representing the "category" of the hand (i.e. 'straight') 
        followed by the cards in sorted order.
        
        The cards are sorted by rank-count (primary key) then by
        rank (secondary key). Note: Aces are ranked '14', so A-2-3-4-5
        is a separately handled edge-case.
        
        The hand: 
            K♠, 2♠, 7♣, 7♦, 2♥, would map to
        -> [3, 7, 7, 2, 2, 13]
        
        
        (1.) '3' is the "category value" of the 'two pair'
             (it is the 3rd worst category of hand)
        (2.) '7' is the first card in the high pair
        (3.) '7' is the second card in the high pair
        (4.) '2' is the first card in the low pair
        (5.) '2' is the second card in the low pair
        (6.) '13' ('King') is the kicker.
        
        The primary-key sort ensures that all of the pair cards precede
        the king even though they are outranked by the king. The
        secondary-key sort ensures that the high-pair cards precede
        the low-pair cards (and that any kicker cards are sorted in 
        descending order of rank)
        
        Once we have this list of integers we convert it into a
        single integer for the sake of efficiently comparing two hands
        to decide which hand wins. The mapping (list of ints) -> int
        preserves cardinality (that is to say, Hand-A beats Hand-B if 
        and only if Hand-A has a higher 'value' than Hand-B.
        '''
        
        self.cards = sorted(self.cards,
                          key=lambda card: card.rank,
                          reverse=True)
        self.cards = sorted(self.cards,
                          key=lambda card: rank_count[card.rank],
                          reverse=True)
        self.cards = list(map(lambda card: card.rank, self.cards))
        # Edge-case: 5 is the high-card in an A, 2, 3, 4, 5 straight
        if {14, 2, 3, 4, 5} < distinct_ranks:
            self.cards = self.cards[1:] + self.cards[0:1]
        is_flush = max({*suit_count.values()}) == 5
        
        # Straight Flush
        if is_straight and is_flush:
            self.value = [STRAIGHT_FLUSH] + self.cards
        # Four-of-a-Kind
        elif rank_count_shape == (4, 1):
            self.value = [FOUR_OF_A_KIND] + self.cards
        # Full House
        elif rank_count_shape == (3, 2):
            self.value = [FULL_HOUSE] + self.cards
        # Flush
        elif is_flush:
            self.value = [FLUSH] + self.cards
        # Straight
        elif is_straight:
            self.value = [STRAIGHT] + self.cards
        # Three-of-a-Kind
        elif rank_count_shape == (3, 1, 1):
            self.value = [THREE_OF_A_KIND] + self.cards
        # Two Pair
        elif rank_count_shape == (2, 2, 1):
            self.value = [TWO_PAIR] + self.cards
        # Pair
        elif rank_count_shape == (2, 1, 1, 1):
            self.value = [PAIR] + self.cards
        # High Card
        else:
            self.value = [HIGH_CARD] + self.cards
        ''' 
        Compute a unique, cardinality-preserving int-value for the hand.
        Note any base >= 15 would have worked (since there are 13 ranks the
        highest of which is assigned a numerical value of 14. We use hex
        because it is built into the language and is therefore the simplest
        cardinality-preserving conversion
        '''
        # hand-value to hex-string, e.g. [1, 14, 10] -> ['1', 'e', 'a']
        self.value = list(map(lambda x: format(x, 'x'), self.value))
        # hex-string to int, e.g. ['1', 'e', 'a'] -> 0x1ea -> 490
        self.value = int(''.join(str(x) for x in self.value), 16)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

def evaluate_pocket(card_1, card_2, num_players=2, num_simulations=NUM_SIMULATIONS):
    if num_players < 2:
        raise ValueError('Must have at least two players')
    print(f'Evaluating pocket: {card_1}{card_2} vs {num_players-1} opponents. {num_simulations} simulations')
    deck = Deck()
    deck.remove(card_1)
    deck.remove(card_2)
    pocket = [card_1, card_2]
    tally = {'wins': 0, 'losses': 0, 'ties': 0}
    for _ in range(num_simulations):
        deck.shuffle()
        pocket_player = pocket + deck[:5]
        all_combos = list(itertools.combinations(pocket_player, 5))
        best_pocket_hand_value = max([Hand(cards).value for cards in all_combos])
        all_opponent_combos = []
        for i in range(num_players-1):
            opponent_i = deck[:5] + deck[5+(2*i):7+(2*i)]
            all_combos = list(itertools.combinations(opponent_i, 5))
            all_opponent_combos.extend(all_combos)
        best_opponent_hand_value = max([Hand(cards).value for cards in all_combos])
        if best_pocket_hand_value > best_opponent_hand_value:
            tally['wins'] += 1
        elif best_pocket_hand_value < best_opponent_hand_value:
            tally['losses'] += 1
        else:
            tally['ties'] += 1
    tally.update((k, v / num_simulations) for k, v in tally.items())
    return tally

ace_of_spades = Card(rank=14, suit='♠')
ace_of_clubs  = Card(rank=14, suit='♣')
bullets = [ace_of_spades, ace_of_clubs]
simulation_results = evaluate_pocket(*bullets, 3, NUM_SIMULATIONS)
print(f'{simulation_results=}')
