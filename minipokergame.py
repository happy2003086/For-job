import random
from itertools import combinations

# 定义牌组
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']

def create_deck():
    """创建一副完整的扑克牌（无花色）"""
    return RANKS * 4  # 每种点数4张

def deal_cards(deck, num_players=2, cards_per_player=13):
    """发牌给玩家"""
    random.shuffle(deck)
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_player):
        for i in range(num_players):
            if deck:
                hands[i].append(deck.pop())
    return hands

def is_single(hand):
    """检查是否为单张"""
    return len(hand) == 1

def is_pair(hand):
    """检查是否为一对"""
    return len(hand) == 2 and hand[0] == hand[1]

def is_triplet(hand):
    """检查是否为三条"""
    return len(hand) == 3 and hand[0] == hand[1] == hand[2]

def is_four_of_a_kind(hand):
    """检查是否为四条"""
    return len(hand) == 4 and hand[0] == hand[1] == hand[2] == hand[3]

def is_straight(hand):
    """检查是否为顺子（五张连续牌）"""
    if len(hand) != 5:
        return False
    
    # 获取牌的等级索引并排序
    indices = sorted([RANKS.index(card) for card in hand])
    
    # 检查是否为连续的数字
    for i in range(1, 5):
        if indices[i] != indices[i-1] + 1:
            return False
    return True

def compare_plays(play1, play2):
    """比较两个牌组的大小"""
    if not play1 or not play2:
        return False
    
    # 比较牌型
    if len(play1) != len(play2):
        return False
    
    # 比较最大的牌
    max1 = max(play1, key=lambda x: RANKS.index(x))
    max2 = max(play2, key=lambda x: RANKS.index(x))
    return RANKS.index(max1) > RANKS.index(max2)

def validate_play(hand, selected_cards):
    """验证玩家选择的牌是否符合规则"""
    if not selected_cards:
        return False
    
    # 检查所选牌是否都在手牌中
    temp_hand = hand.copy()
    for card in selected_cards:
        if card in temp_hand:
            temp_hand.remove(card)
        else:
            return False
    
    if len(selected_cards) == 1:
        return is_single(selected_cards)
    elif len(selected_cards) == 2:
        return is_pair(selected_cards)
    elif len(selected_cards) == 3:
        return is_triplet(selected_cards)
    elif len(selected_cards) == 4:
        return is_four_of_a_kind(selected_cards)
    elif len(selected_cards) == 5:
        return is_straight(selected_cards)
    return False

def computer_play(hand, last_play=None):
    """改进的电脑出牌逻辑，会尽量出牌并遵守规则"""
    possible_plays = []
    
    # 生成所有可能的合法出牌
    for n in range(1, 6):
        if n > len(hand):
            continue
        
        for combo in combinations(hand, n):
            combo = list(combo)
            valid = False
            
            if n == 1:
                valid = is_single(combo)
            elif n == 2:
                valid = is_pair(combo)
            elif n == 3:
                valid = is_triplet(combo)
            elif n == 4:
                valid = is_four_of_a_kind(combo)
            elif n == 5:
                valid = is_straight(combo)
            
            if valid:
                # 如果没有上家出牌，或者能压过上家的牌
                if not last_play or (len(combo) == len(last_play) and compare_plays(combo, last_play)):
                    possible_plays.append(combo)
    
    if not possible_plays:
        return []  # 没有能出的牌
    
    # 优先出能减少最多手牌的牌
    possible_plays.sort(key=lambda x: -len(x))
    
    # 在相同长度的牌中，优先出点数大的牌
    possible_plays.sort(key=lambda x: (-len(x), -max(RANKS.index(c) for c in x)))
    
    return possible_plays[0]

def print_hand(hand):
    """打印手牌"""
    print(" ".join(sorted(hand, key=lambda x: RANKS.index(x))))

def print_game_state(player_hand, computer_hand, player_name="玩家", computer_name="电脑"):
    """显示游戏状态"""
    print(f"\n{player_name}的手牌({len(player_hand)}张): ", end="")
    print_hand(player_hand)
    print(f"{computer_name}的手牌({len(computer_hand)}张): ", end="")
    print_hand(computer_hand)

def get_player_move(hand):
    """获取玩家出牌选择"""
    while True:
        print("\n你的手牌: ", end="")
        print_hand(sorted(hand, key=lambda x: RANKS.index(x)))
        choice = input("请选择要出的牌（用空格分隔，例如'3 3'），或输入'pass'跳过: ")
        
        if choice.lower() == 'pass':
            return []
        
        selected = choice.split()
        if validate_play(hand, selected):
            return selected
        else:
            print("输入无效或不符合出牌规则，请重新输入！")

def play_game():
    """主游戏流程"""
    print("欢迎来到扑克游戏！")
    print("游戏规则：每人13张牌，可以出单张、对子、三条、四条或五张顺子")
    print("出牌必须与上家牌型相同且更大，或者选择跳过")
    
    # 创建并发牌
    deck = create_deck()
    player_hand, computer_hand = deal_cards(deck)
    
    # 排序手牌便于查看
    player_hand.sort(key=lambda x: RANKS.index(x))
    computer_hand.sort(key=lambda x: RANKS.index(x))
    
    current_player = random.randint(0, 1)  # 随机决定谁先出牌
    last_play = None
    consecutive_passes = 0  # 记录连续跳过的次数
    
    while player_hand and computer_hand:
        print_game_state(player_hand, computer_hand)
        
        if current_player == 0:
            # 玩家回合
            print("\n=== 你的回合 ===")
            selected = get_player_move(player_hand)
            
            if selected:
                # 从手牌中移除已出的牌
                for card in selected:
                    player_hand.remove(card)
                last_play = selected
                print(f"\n你出了: {' '.join(selected)}")
                consecutive_passes = 0
            else:
                print("\n你选择了跳过")
                consecutive_passes += 1
        else:
            # 电脑回合
            print("\n=== 电脑回合 ===")
            selected = computer_play(computer_hand, last_play)
            
            if selected:
                # 从手牌中移除已出的牌
                for card in selected:
                    computer_hand.remove(card)
                last_play = selected
                print(f"电脑出了: {' '.join(selected)}")
                consecutive_passes = 0
            else:
                print("电脑选择了跳过")
                consecutive_passes += 1
        
        # 如果连续两家都跳过，清除上家出牌
        if consecutive_passes >= 2:
            last_play = None
            consecutive_passes = 0
            print("\n两家都跳过，重新开始出牌！")
        
        # 切换玩家
        current_player = 1 - current_player
        
        # 检查游戏是否结束
        if not player_hand:
            print("\n恭喜！你出完了所有牌，你赢了！")
            break
        if not computer_hand:
            print("\n电脑出完了所有牌，你输了！")
            break

if __name__ == "__main__":
    play_game()