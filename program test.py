import random

# 自動生成 100 條填空題
questions = []

# 變數操作
for i in range(1, 101):
    if i % 5 == 0:
        question = {
            "question": f"填入缺失的代碼，使程式輸出 '數字：{i}'：\n```python\nprint('數字：' + ___)\n```", 
            "answer": f"'{i}'"
        }
        questions.append(question)
    
# 基本數學運算
for i in range(1, 101):
    if i % 4 == 0:
        question = {
            "question": f"填入缺失的代碼，使程式計算 {i} 加 50 並輸出：\n```python\nresult = {i} + ___\nprint(result)\n```", 
            "answer": "50"
        }
        questions.append(question)

# 字符串處理
for i in range(1, 101):
    if i % 3 == 0:
        question = {
            "question": f"填入缺失的代碼，使程式將 '編程' 和數字 {i} 組合並輸出：\n```python\nresult = '編程' + str(___)\nprint(result)\n```", 
            "answer": str(i)
        }
        questions.append(question)

# 列表操作
for i in range(1, 101):
    if i % 6 == 0:
        question = {
            "question": f"填入缺失的代碼，將數字 {i} 添加到列表 [1, 2, 3] 並輸出列表：\n```python\nmy_list = [1, 2, 3]\nmy_list.append(___)\nprint(my_list)\n```", 
            "answer": str(i)
        }
        questions.append(question)

# 判斷語句
for i in range(1, 101):
    if i % 7 == 0:
        question = {
            "question": f"填入缺失的代碼，判斷 {i} 是否為偶數，並輸出結果：\n```python\nif ___ % 2 == 0:\n    print('偶數')\nelse:\n    print('奇數')\n```", 
            "answer": str(i)
        }
        questions.append(question)

# 循環
for i in range(1, 101):
    if i % 8 == 0:
        question = {
            "question": f"填入缺失的代碼，使用循環打印 1 到 {i} 的所有數字：\n```python\nfor num in range(1, ___ + 1):\n    print(num)\n```", 
            "answer": str(i)
        }
        questions.append(question)

# 函數操作
for i in range(1, 101):
    if i % 9 == 0:
        question = {
            "question": f"填入缺失的代碼，定義一個函數返回 {i} 的平方並輸出：\n```python\ndef square(x):\n    return ___\nprint(square({i}))\n```", 
            "answer": str(i**2)
        }
        questions.append(question)

# 隨機排序題目
random.shuffle(questions)

# 啟動遊戲
def play_game():
    print("歡迎來到填空題編程遊戲！")
    score = 0
    total_questions = 0
    
    for idx, q in enumerate(questions, start=1):
        print(f"\n問題 {idx}:")
        print(q["question"])
        user_answer = input("請填寫答案（輸入 'quit' 隨時退出遊戲）：")

        if user_answer.strip().lower() == "quit":
            print(f"\n遊戲已退出！你當前得到了 {score} 分，總共有 {total_questions} 題。")
            print(f"你的得分率是 {score/total_questions * 100}%")
            break

        if user_answer.strip() != "":
            total_questions += 1
            if user_answer.strip() == q["answer"]:
                print("正確！")
                score += 1
            else:
                print(f"錯誤，正確答案是：{q['answer']}")
        else:
            print("未作答，跳過此題。")

    else:
        # 如果遊戲正常結束，顯示最終得分
        print(f"\n遊戲結束！你得到了 {score} 分，總共答對 {score} 題，總共答過 {total_questions} 題。")
        print(f"你的得分率是 {score/total_questions * 100}%")

# 啟動遊戲
play_game()
