import random
import os
import time

def clear_screen():
    """清除終端畫面"""
    os.system('cls' if os.name == 'nt' else 'clear')

def number_memory_game():
    length = random.randint(1, 8)  # 隨機決定數字長度
    number = ''.join(str(random.randint(0, 9)) for _ in range(length))  # 生成隨機數字
    
    print(f"記住這個數字: {number}")
    time.sleep(2)  # 顯示 2 秒
    clear_screen()

    user_input = input("請輸入剛剛的數字: ")
    
    if user_input == number:
        print("答對了！你的記憶力不錯！")
    else:
        print(f"答錯了，正確答案是 {number}")

if __name__ == "__main__":
    number_memory_game()
