import itertools
import time

def is_royal_flush(hand):
    ranks = {card[0] for card in hand}
    suits = {card[1] for card in hand}
    return ranks == {10, 11, 12, 13, 14} and len(suits) == 1

def is_straight_flush(hand):
    ranks = sorted(card[0] for card in hand)
    suits = {card[1] for card in hand}
    return len(suits) == 1 and ranks == list(range(ranks[0], ranks[0] + 5))

def is_four_of_a_kind(hand):
    ranks = [card[0] for card in hand]
    return any(ranks.count(rank) == 4 for rank in set(ranks))

def is_full_house(hand):
    ranks = [card[0] for card in hand]
    return len(set(ranks)) == 2 and any(ranks.count(rank) == 3 for rank in set(ranks))

def is_flush(hand):
    suits = {card[1] for card in hand}
    ranks = sorted(card[0] for card in hand)
    return len(suits) == 1 and ranks != list(range(ranks[0], ranks[0] + 5)) #排除同花順

def is_straight(hand):
    ranks = sorted(card[0] for card in hand)
    suits = {card[1] for card in hand}
    return len(suits) != 1 and ranks == list(range(ranks[0], ranks[0] + 5)) #排除同花順

def is_three_of_a_kind(hand):
    ranks = [card[0] for card in hand]
    return any(ranks.count(rank) == 3 for rank in set(ranks)) and len(set(ranks)) != 2 #排除Full House

def is_two_pair(hand):
    ranks = [card[0] for card in hand]
    count = 0
    for rank in set(ranks):
        if ranks.count(rank) == 2:
            count += 1
    return count == 2

def is_one_pair(hand):
    ranks = [card[0] for card in hand]
    return any(ranks.count(rank) == 2 for rank in set(ranks)) and len(set(ranks)) == 4

def is_high_card(hand):
    ranks = sorted(card[0] for card in hand)
    suits = {card[1] for card in hand}
    straight = ranks == list(range(ranks[0], ranks[0] + 5))
    flush = len(suits) == 1
    return not (straight or flush or any(ranks.count(rank) >= 2 for rank in set(ranks)))

def calculate_probabilities():
    deck = [(rank, suit) for rank in range(2, 15) for suit in 'SHDC']
    all_hands = list(itertools.combinations(deck, 5))
    total_hands = len(all_hands)

    counts = {
        'royal_flush': 0, 'straight_flush': 0, 'four_of_a_kind': 0,
        'full_house': 0, 'flush': 0, 'straight': 0,
        'three_of_a_kind': 0, 'two_pair': 0, 'one_pair': 0, 'high_card': 0
    }

    start_time = time.time()
    for i, hand in enumerate(all_hands):
        if is_royal_flush(hand): counts['royal_flush'] += 1
        elif is_straight_flush(hand): counts['straight_flush'] += 1
        elif is_four_of_a_kind(hand): counts['four_of_a_kind'] += 1
        elif is_full_house(hand): counts['full_house'] += 1
        elif is_flush(hand): counts['flush'] += 1
        elif is_straight(hand): counts['straight'] += 1
        elif is_three_of_a_kind(hand): counts['three_of_a_kind'] += 1
        elif is_two_pair(hand): counts['two_pair'] += 1
        elif is_one_pair(hand): counts['one_pair'] += 1
        elif is_high_card(hand): counts['high_card'] += 1

        if (i + 1) % (total_hands // 100) == 0 or i == total_hands - 1:
            percentage = (i + 1) / total_hands * 100
            elapsed_time = time.time() - start_time
            print(f"進度: {percentage:.2f}%，已用時間: {elapsed_time:.2f} 秒", end='\r')

    print()

    probabilities = {hand: count / total_hands for hand, count in counts.items()}
    return probabilities

probabilities = calculate_probabilities()
for hand_type, prob in probabilities.items():
    print(f"{hand_type} 的概率: {prob:.10f}")
