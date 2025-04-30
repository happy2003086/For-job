import time
import random
import threading

def wait_for_input():
    input("數字相同了！按 Enter 發射！")

def play_game():
    score = 0
    time_limit = 1  # 每秒更新數字
    reaction_limit = 2  # 反應時間限制改為2秒
    print("歡迎來到射箭遊戲！當出現兩位數字並且兩個數字相同時，按 Enter 發射！錯過會扣分！")
    time.sleep(2)  # 給玩家準備的時間
    try:
        while True:
            # 隨機生成一個兩位數字
            num = random.randint(10, 99)  # 生成 10 到 99 的隨機數字
            tens = num // 10  # 取得十位數
            ones = num % 10   # 取得個位數

            print(f"數字: {num}")
            start_time = time.time()  # 記錄數字出現的時間

            # 只有當十位數和個位數相同時，才可以按 Enter 發射
            while tens != ones:
                num = random.randint(10, 99)  # 重新生成數字
                tens = num // 10
                ones = num % 10
                print(f"數字: {num}")
                time.sleep(time_limit)  # 每秒更新一次數字

            # 記錄開始的時間
            reaction_start_time = time.time()
            # 啟動另一個線程等待玩家按 Enter
            input_thread = threading.Thread(target=wait_for_input)
            input_thread.start()

            # 等待玩家完成輸入或時間過期
            input_thread.join(timeout=reaction_limit)  # 限制時間為reaction_limit

            # 計算反應時間
            reaction_time = time.time() - reaction_start_time

            # 如果玩家按下 Enter 且反應時間在限制時間內
            if input_thread.is_alive():
                print(f"錯過了！當前得分: {score}")
                score -= 1  # 沒有按下 Enter 在時間內算錯過
            else:
                if reaction_time < reaction_limit:  # 反應時間小於2秒
                    score += 1
                    print(f"成功發射！當前得分: {score}")
                else:
                    score -= 1
                    print(f"反應太慢！扣分！當前得分: {score}")
            
            time.sleep(time_limit)  # 等待下一輪

    except KeyboardInterrupt:
        print("\n遊戲結束！最終得分是:", score)

if __name__ == "__main__":
    play_game()
