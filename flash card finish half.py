import random
import tkinter as tk
from tkinter import messagebox

# 定義一副牌
def create_deck():
    # 減少字母種類（A-F），每種 2 張，總共 12 張牌
    deck = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F']
    random.shuffle(deck)  # 隨機洗牌
    return deck

# 顯示翻開的牌結果
def display_revealed():
    for i, button in enumerate(buttons):
        if revealed[i]:
            button.config(text=deck[i], state=tk.DISABLED)  # 顯示牌面並禁用按鈕
        else:
            button.config(text="X", state=tk.NORMAL)  # 顯示隱藏符號並啟用按鈕

# 玩家點擊牌
def on_card_click(index):
    global first_choice, second_choice, score_player, score_computer, player_turn

    if not player_turn:  # 如果不是玩家回合，忽略點擊
        return

    if first_choice is None:  # 選擇第一張牌
        first_choice = index
        buttons[first_choice].config(text=deck[first_choice], state=tk.DISABLED)
        # 更新電腦的記憶
        update_computer_memory(first_choice, deck[first_choice])
    else:  # 選擇第二張牌
        second_choice = index
        buttons[second_choice].config(text=deck[second_choice], state=tk.DISABLED)
        # 更新電腦的記憶
        update_computer_memory(second_choice, deck[second_choice])
        root.after(1000, check_match)  # 1 秒後檢查是否配對

# 檢查是否配對
def check_match():
    global first_choice, second_choice, score_player, score_computer, player_turn

    if deck[first_choice] == deck[second_choice]:  # 配對成功
        revealed[first_choice] = True
        revealed[second_choice] = True
        if player_turn:
            score_player += 1
            messagebox.showinfo("配對成功", "玩家配對成功！")
        else:
            score_computer += 1
            messagebox.showinfo("配對成功", "電腦配對成功！")
    else:  # 配對失敗
        buttons[first_choice].config(text="X", state=tk.NORMAL)
        buttons[second_choice].config(text="X", state=tk.NORMAL)
        messagebox.showinfo("配對失敗", "配對失敗，請再試！")

    first_choice, second_choice = None, None
    update_score()
    if all(revealed):  # 如果所有牌都已翻開，遊戲結束
        end_game()
    else:
        if player_turn:  # 如果是玩家回合，切換到電腦回合
            player_turn = False
            root.after(1000, computer_turn)  # 1 秒後開始電腦回合
        else:  # 如果是電腦回合，切換到玩家回合
            player_turn = True
            messagebox.showinfo("玩家回合", "請選擇兩張牌！")

# 更新分數顯示
def update_score():
    score_label.config(text=f"玩家分數: {score_player}  電腦分數: {score_computer}")

# 更新電腦的記憶
def update_computer_memory(index, card):
    if card in computer_memory:
        computer_memory[card].append(index)
    else:
        computer_memory[card] = [index]

# 電腦回合（根據記憶選擇）
def computer_turn():
    global first_choice, second_choice

    # 檢查是否有已知的配對
    for card, indices in computer_memory.items():
        if len(indices) == 1:  # 如果有一張已知的牌，找出配對的牌
            remaining_choices = [i for i in range(len(deck)) if not revealed[i] and i != indices[0]]
            first_choice, second_choice = indices[0], random.choice(remaining_choices)
            break
    else:  # 如果沒有已知的配對，隨機選擇兩張牌
        available_choices = [i for i in range(len(deck)) if not revealed[i]]
        first_choice, second_choice = random.sample(available_choices, 2)

    # 顯示電腦的選擇
    buttons[first_choice].config(text=deck[first_choice], state=tk.DISABLED)
    buttons[second_choice].config(text=deck[second_choice], state=tk.DISABLED)
    # 更新電腦的記憶
    update_computer_memory(first_choice, deck[first_choice])
    update_computer_memory(second_choice, deck[second_choice])
    root.after(1000, check_match)  # 1 秒後檢查是否配對

# 結束遊戲
def end_game():
    if score_player > score_computer:
        messagebox.showinfo("遊戲結束", f"恭喜你贏了！\n玩家分數: {score_player}  電腦分數: {score_computer}")
    elif score_player < score_computer:
        messagebox.showinfo("遊戲結束", f"電腦贏了！\n玩家分數: {score_player}  電腦分數: {score_computer}")
    else:
        messagebox.showinfo("遊戲結束", f"平手！\n玩家分數: {score_player}  電腦分數: {score_computer}")
    root.quit()

# 初始化遊戲
def init_game():
    global deck, revealed, buttons, first_choice, second_choice, score_player, score_computer, player_turn, computer_memory
    deck = create_deck()
    revealed = [False] * len(deck)
    first_choice, second_choice = None, None
    score_player, score_computer = 0, 0
    player_turn = True
    computer_memory = {}  # 初始化電腦的記憶

    for button in buttons:
        button.destroy()
    buttons.clear()

    for i in range(len(deck)):
        button = tk.Button(root, text="X", font=("Arial", 12), width=4, height=2,
                          command=lambda i=i: on_card_click(i))
        button.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        buttons.append(button)

    update_score()
    messagebox.showinfo("玩家回合", "請選擇兩張牌！")

# 主程式
root = tk.Tk()
root.title("記憶配對遊戲")

# 設置窗口大小
root.geometry("300x400")  # 適合手機屏幕的大小

buttons = []
score_label = tk.Label(root, text="玩家分數: 0  電腦分數: 0", font=("Arial", 12))
score_label.grid(row=3, column=0, columnspan=4, pady=10)

init_button = tk.Button(root, text="重新開始", font=("Arial", 12), command=init_game)
init_button.grid(row=4, column=0, columnspan=4, pady=10)

init_game()  # 初始化遊戲

root.mainloop()
