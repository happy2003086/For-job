import random
import time

def generate_question():
    operator = random.choice(['+', '-', '*'])
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    question = f"{num1} {operator} {num2} = ?"
    answer = eval(f"{num1} {operator} {num2}")
    return question, answer

def play_game():
    correct_count = 0
    total_count = 0
    start_time = time.time()

    while time.time() - start_time < 60:  # 遊戲時間限制為 60 秒
        question, answer = generate_question()
        print(question)

        start_answer_time = time.time()  # 記錄回答開始時間
        user_answer = input("請在五秒內回答：")

        if user_answer.lower() == 'q':  # 按下 'q' 結束遊戲
            break

        if time.time() - start_answer_time > 5:  # 檢查是否超過五秒
            print("回答時間超過限制，遊戲結束！")
            break

        try:
            user_answer = int(user_answer)
            if user_answer == answer:
                print("答對了！")
                correct_count += 1
            else:
                print(f"答錯了，答案是 {answer}")
        except ValueError:
            print("請輸入數字！")

        total_count += 1

    if total_count > 0:
        accuracy = correct_count / total_count * 100
        print(f"遊戲結束，正確率為 {accuracy:.2f}%")
    else:
        print("遊戲結束，沒有回答任何問題。")

play_game()