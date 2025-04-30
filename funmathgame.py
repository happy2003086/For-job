import random

def generate_numbers():
    return [random.randint(1, 10) for _ in range(4)]

def check_24(expression, numbers):
    try:
        # 確保玩家輸入嘅數字正確（避免用錯其他數字）
        used_numbers = [int(n) for n in expression if n.isdigit()]
        if sorted(used_numbers) != sorted(numbers):
            print("❌ 你輸入的數字不匹配！")
            return False
        
        # 計算結果
        result = eval(expression)
        if result == 24:
            print("✅ 恭喜！你計算正確！")
            return True
        else:
            print(f"❌ 答案錯誤，計算結果為 {result}")
            return False
    except Exception as e:
        print(f"❌ 計算錯誤：{e}")
        return False

# 遊戲開始
numbers = generate_numbers()
print("你的數字是：", numbers)

user_input = input("請輸入你的計算表達式（例如：(8 / 2) * (3 + 1)）：")
check_24(user_input, numbers)
