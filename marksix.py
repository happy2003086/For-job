import random
import time

def generate_lottery_numbers():
    """隨機生成六個號碼"""
    numbers = random.sample(range(1, 50), 6)
    numbers.sort()
    return numbers

def calculate_prizes(winning_numbers, player_numbers):
    """計算中獎情況和獎金"""
    matched_numbers = set(winning_numbers) & set(player_numbers)
    count = len(matched_numbers)
    
    # 假設獎金規則
    prizes = {
        6: 10000000,  # 中六獎
        5: 100000,    # 中五獎
        4: 3000,      # 中四獎
        3: 200,       # 中三獎
        2: 10,        # 中二獎
    }
    
    return count, prizes.get(count, 0)

def main():
    # 讓用戶輸入初始金額
    initial_amount = int(input("請輸入您的初始金額："))
    current_amount = initial_amount
    
    total_draws = 0
    total_wins = 0
    prize_count = {i: 0 for i in range(2, 7)}  # 紀錄每種獎項的次數

    print("歡迎來到六合彩模擬程式！")
    print(f"您的初始金額：{initial_amount} 元")
    
    while current_amount > 0:
        total_draws += 1
        winning_numbers = generate_lottery_numbers()
        print(f"\n本期開獎號碼：{winning_numbers}")
        
        player_numbers = generate_lottery_numbers()
        print(f"您的號碼：{player_numbers}")
        
        count, prize = calculate_prizes(winning_numbers, player_numbers)
        
        if prize > 0:
            total_wins += 1
            prize_count[count] += 1  # 增加對應獎項的中獎次數
            current_amount += prize
            print(f"恭喜！您中獎了 {count} 個號碼，獲得獎金：{prize} 元！")
        else:
            current_amount -= 10  # 假設每次參加抽獎需扣除 10 元
            print("很遺憾，您沒有中獎。")
        
        print(f"您目前的金額：{current_amount} 元")
        
        time.sleep(1)  # 暫停一秒，讓輸出更易讀

    # 計算中獎百分比
    win_percentage = (total_wins / total_draws) * 100 if total_draws > 0 else 0
    print(f"\n遊戲結束！")
    print(f"總共抽獎次數：{total_draws}")
    print(f"中獎次數：{total_wins}")
    print(f"中獎百分比：{win_percentage:.2f}%")
    
    # 顯示各獎項中獎次數及其百分比
    for i in range(2, 7):
        if total_wins > 0:
            prize_percentage = (prize_count[i] / total_wins) * 100
        else:
            prize_percentage = 0
        print(f"中{i}獎次數：{prize_count[i]}，佔總中獎次數的百分比：{prize_percentage:.2f}%")

if __name__ == "__main__":
    main()
