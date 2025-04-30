import random

def deal_cards():
    """隨機發牌，兩張手牌與一張第三張牌"""
    deck = list(range(1, 14)) * 4  # 撲克牌點數，1-13（A=1，J=11，Q=12，K=13）
    random.shuffle(deck)  # 洗牌
    return deck[:3]  # 發前三張牌

def shoot_the_dragon(cards):
    """根據規則判斷是否射龍門獲勝"""
    card1, card2, card3 = cards
    print(f"\n手牌1: {card1}, 手牌2: {card2}, 第三張牌: {card3}")
    
    # 判斷第三張牌是否介於前兩張牌之間
    if min(card1, card2) < card3 < max(card1, card2):
        return "恭喜，射龍門成功！"
    else:
        return "很遺憾，未能射龍門。"

def play_game():
    """控制遊戲循環"""
    while True:
        cards = deal_cards()  # 發牌
        result = shoot_the_dragon(cards)  # 判斷結果
        print(result)

        # 讓玩家選擇是否繼續
        choice = input("\n按任意鍵繼續，輸入 'q' 退出：")
        if choice.lower() == 'q':
            print("遊戲結束，感謝遊玩！")
            break

# 執行遊戲
play_game()
