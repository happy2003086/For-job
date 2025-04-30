def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

while True:
    try:
        # 輸入兩個數字
        num1 = int(input("請輸入第一個數字（或輸入 'q' 退出）: "))
        if str(num1).lower() == 'q':
            print("程式結束！")
            break
        
        num2 = int(input("請輸入第二個數字: "))
        
        # 計算並輸出結果
        print(f"\n最大公因數 (GCD): {gcd(num1, num2)}")
        print(f"最小公倍數 (LCM): {lcm(num1, num2)}\n")
    
    except ValueError:
        print("請輸入有效的整數！")
        