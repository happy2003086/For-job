import random
import time
import os

# 定義一副牌
def create_deck():
    # 減少字母種類（A-F），每種 2 張，總共 12 張牌
    deck = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F']
    random.shuffle(deck)  # 隨機洗牌
    return deck

# 顯示翻開的牌結果（排列成 3x4 的矩陣）
def display_revealed(deck, revealed):
    print("\n牌面:")
    for i in range(0, len(deck), 4):  # 每行顯示 4 張牌
        row = deck[i:i+4]  # 獲取當前行
        revealed_row = revealed[i:i+4]  # 獲取當前行是否翻開
        for j in range(len(row)):
            if revealed_row[j]:
                print(f"[{i+j+1:2}:{row[j]}]", end="  ")  # 顯示牌面和編號
            else:
                print(f"[{i+j+1:2}: X ]", end="  ")  # 顯示牌號和隱藏符號
        print()  # 換行
    print()  # 換行

# 清屏函數，根據操作系統選擇清屏命令
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 玩家選擇兩張牌
def player_turn(deck, revealed):
    available_choices = [i for i in range(len(deck)) if not revealed[i]]  # 找到還沒翻開的牌
    print("\n請選擇兩張牌：")
    
    while True:
        try:
            first_choice = int(input(f"選擇第一張牌 (1-{len(deck)}): ")) - 1
            second_choice = int(input(f"選擇第二張牌 (1-{len(deck)}): ")) - 1

            # 檢查輸入是否有效
            if first_choice == second_choice:
                print("不能選擇同一張牌，請重新選擇！")
            elif first_choice < 0 or second_choice < 0 or first_choice >= len(deck) or second_choice >= len(deck):
                print("請輸入有效的牌號！")
            elif revealed[first_choice] or revealed[second_choice]:
                print("這兩張牌已經翻開，請選擇其他牌！")
            else:
                return first_choice, second_choice
        except ValueError:  # 如果輸入的不是數字
            print("請輸入數字！")

# 電腦選擇兩張牌（改進版：有記憶功能）
def computer_turn(deck, revealed, memory):
    available_choices = [i for i in range(len(deck)) if not revealed[i]]  # 找到還沒翻開的牌
    if len(available_choices) < 2:
        return None, None  # 如果只剩下一張或沒有未翻開的牌，結束遊戲

    # 檢查是否有已知的配對
    for card in memory:
        if memory[card] >= 2:  # 如果知道兩張相同的牌
            choices = [i for i, x in enumerate(deck) if x == card and not revealed[i]]
            if len(choices) >= 2:
                return choices[0], choices[1]

    # 如果沒有已知的配對，隨機選擇兩張牌
    first_choice = random.choice(available_choices)
    available_choices.remove(first_choice)  # 移除已選的牌，確保第二張不同
    second_choice = random.choice(available_choices)
    
    return first_choice, second_choice

# 主遊戲邏輯
def play_game():
    deck = create_deck()  # 創建牌
    revealed = [False] * len(deck)  # 用來追蹤哪些牌已經翻開
    memory = {}  # 電腦的記憶，記錄每張牌的位置
    score_player = 0
    score_computer = 0
    turns = 0
    
    while False in revealed:  # 還有牌沒有翻開的話，繼續
        print(f"\n當前玩家分數: {score_player}  電腦分數: {score_computer}")
        
        # 玩家回合
        print("\n玩家回合！")
        first_choice, second_choice = player_turn(deck, revealed)
        
        if first_choice is None or second_choice is None:
            continue
        
        # 玩家翻開兩張牌並直接顯示結果
        revealed[first_choice] = True
        revealed[second_choice] = True
        display_revealed(deck, revealed)
        time.sleep(3)  # 顯示結果 3 秒
        clear_screen()  # 清除屏幕
        
        # 如果兩張牌相同，加分
        if deck[first_choice] == deck[second_choice]:
            print("配對成功！")
            score_player += 1  # 玩家加分
        else:
            print("配對失敗，請再試！")
            revealed[first_choice] = False
            revealed[second_choice] = False
        
        # 檢查是否所有牌都已翻開
        if False not in revealed:
            break
        
        # 電腦回合
        print("\n電腦回合！")
        time.sleep(1)  # 模擬思考時間
        first_choice, second_choice = computer_turn(deck, revealed, memory)
        
        if first_choice is None or second_choice is None:
            break  # 如果只剩一張牌，遊戲結束

        # 電腦翻開兩張牌並直接顯示結果
        revealed[first_choice] = True
        revealed[second_choice] = True
        display_revealed(deck, revealed)
        time.sleep(3)  # 顯示結果 3 秒
        clear_screen()  # 清除屏幕

        # 如果兩張牌相同，電腦加分
        if deck[first_choice] == deck[second_choice]:
            print("電腦配對成功！")
            score_computer += 1  # 電腦加分
        else:
            print("電腦配對失敗，請再試！")
            revealed[first_choice] = False
            revealed[second_choice] = False
        
        # 更新電腦的記憶
        for choice in [first_choice, second_choice]:
            card = deck[choice]
            if card in memory:
                memory[card] += 1
            else:
                memory[card] = 1
        
        turns += 1  # 記錄總回合數
    
    print(f"\n遊戲結束！")
    print(f"玩家總分: {score_player}")
    print(f"電腦總分: {score_computer}")
    if score_player > score_computer:
        print("恭喜你贏了！")
    elif score_player < score_computer:
        print("電腦贏了！")
    else:
        print("平手！")

# 開始遊戲
if __name__ == "__main__":
    play_game()