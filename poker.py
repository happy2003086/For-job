import random

# 定义牌型和花色
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_values = {rank: index for index, rank in enumerate(ranks, start=2)}

deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

# 洗牌
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# 发牌
def deal_cards(deck, num_cards):
    return [deck.pop() for _ in range(num_cards)]

# 计算手牌强度（改进版）
def evaluate_hand(hand):
    """
    计算手牌强度，返回手牌类型和数值（用于比较）
    """
    rank_counts = {}
    suit_counts = {}
    rank_list = []

    for card in hand:
        rank = card['rank']
        suit = card['suit']
        rank_list.append(rank_values[rank])
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
        suit_counts[suit] = suit_counts.get(suit, 0) + 1

    rank_list.sort()
    is_flush = max(suit_counts.values()) >= 5
    is_straight = any(
        rank_list[i] == rank_list[i - 1] + 1 for i in range(1, len(rank_list))
    )

    # 牌型优先级（数值越大代表越强）
    if is_flush and is_straight:
        return (8, max(rank_list))  # 同花顺
    elif 4 in rank_counts.values():
        return (7, max(rank_list))  # 四条
    elif sorted(rank_counts.values()) == [2, 3]:
        return (6, max(rank_list))  # 葫芦
    elif is_flush:
        return (5, max(rank_list))  # 同花
    elif is_straight:
        return (4, max(rank_list))  # 顺子
    elif 3 in rank_counts.values():
        return (3, max(rank_list))  # 三条
    elif list(rank_counts.values()).count(2) == 2:
        return (2, max(rank_list))  # 两对
    elif 2 in rank_counts.values():
        return (1, max(rank_list))  # 一对
    else:
        return (0, max(rank_list))  # 高牌

# 显示手牌和公共牌
def display_hands(player_hand, community_cards):
    print("\nYour hand:", player_hand)
    print("Community cards:", community_cards)

# 玩家操作
def player_action():
    while True:
        action = input("Choose action (check/call, bet/raise, fold): ").strip().lower()
        if action in ['check', 'call', 'bet', 'raise', 'fold']:
            return action
        else:
            print("Invalid action. Please choose 'check/call', 'bet/raise', or 'fold'.")

# AI操作（简单逻辑）
def ai_action(ai_strength):
    if ai_strength[0] >= 4:  # 如果AI手牌较强，加注或跟注
        return random.choice(['bet', 'raise', 'call'])
    else:  # 否则随机选择弃牌或跟注
        return random.choice(['fold', 'call'])

# 主游戏循环
def play_poker():
    global deck
    while True:
        deck = shuffle_deck(deck.copy())
        player_chips = 1000  # 玩家初始筹码
        ai_chips = 1000  # AI初始筹码
        pot = 0  # 底池
        current_bet = 0  # 当前注额

        player_hand = deal_cards(deck, 2)
        ai_hand = deal_cards(deck, 2)
        community_cards = deal_cards(deck, 5)

        print("\n--- New Round ---")
        print(f"Your chips: {player_chips}")
        print(f"AI chips: {ai_chips}")

        # 显示初始手牌和公共牌
        display_hands(player_hand, community_cards)

        # 玩家和AI轮流操作
        while True:
            # 玩家操作
            print(f"\nCurrent pot: {pot}")
            print(f"Current bet to call: {current_bet}")
            action = player_action()

            if action == 'fold':
                print("You folded! AI wins the pot.")
                ai_chips += pot
                break
            elif action in ['bet', 'raise']:
                bet_amount = int(input("Enter bet amount: "))
                if bet_amount > player_chips:
                    print("Not enough chips! All-in.")
                    bet_amount = player_chips
                player_chips -= bet_amount
                pot += bet_amount
                current_bet = bet_amount
            elif action in ['check', 'call']:
                if current_bet > 0:
                    player_chips -= current_bet
                    pot += current_bet

            # AI操作
            ai_full_hand = ai_hand + community_cards
            ai_strength = evaluate_hand(ai_full_hand)
            ai_action_taken = ai_action(ai_strength)

            print(f"\nAI chooses to: {ai_action_taken}")
            if ai_action_taken == 'fold':
                print("AI folded! You win the pot.")
                player_chips += pot
                break
            elif ai_action_taken in ['bet', 'raise']:
                ai_bet = random.randint(10, min(100, ai_chips))
                print(f"AI bets {ai_bet} chips.")
                ai_chips -= ai_bet
                pot += ai_bet
                current_bet = ai_bet
            elif ai_action_taken == 'call':
                if current_bet > 0:
                    ai_chips -= current_bet
                    pot += current_bet

            # 显示当前筹码和底池
            print(f"\nYour chips: {player_chips}")
            print(f"AI chips: {ai_chips}")
            print(f"Pot: {pot}")

            # 如果双方都选择check/call，进入比牌阶段
            if action in ['check', 'call'] and ai_action_taken == 'call':
                player_full_hand = player_hand + community_cards
                player_strength = evaluate_hand(player_full_hand)
                ai_strength = evaluate_hand(ai_full_hand)

                print("\n--- Showdown ---")
                print("Your hand:", player_full_hand)
                print("AI hand:", ai_full_hand)
                print("Your hand strength:", player_strength)
                print("AI hand strength:", ai_strength)

                if player_strength > ai_strength:
                    print("You win the pot!")
                    player_chips += pot
                elif player_strength < ai_strength:
                    print("AI wins the pot!")
                    ai_chips += pot
                else:
                    print("It's a tie! Pot is split.")
                    player_chips += pot // 2
                    ai_chips += pot // 2
                break

        # 检查筹码是否耗尽
        if player_chips <= 0:
            print("\nYou are out of chips! Game over.")
            break
        elif ai_chips <= 0:
            print("\nAI is out of chips! You win!")
            break

        # 询问是否继续
        play_again = input("\nDo you want to play another round? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye!")
            break

# 运行游戏
play_poker()