def count_digits(input_string):
    digit_counts = {str(i): 0 for i in range(10)}  # 初始化0-9的计数器
    
    for char in input_string:
        if char.isdigit():  # 检查是否是数字
            digit_counts[char] += 1
    
    return digit_counts

# 获取用户输入
user_input = input("请输入一个字符串：")

# 计算各数字的数量
digit_counts = count_digits(user_input)

# 输出结果
print("数字统计结果：")
for num, count in digit_counts.items():
    print(f"'{num}': {count} 次")