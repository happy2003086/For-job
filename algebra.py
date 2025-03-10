import sympy as sp

# 定義變數
a, b = sp.symbols('a b')

# 提示用戶輸入方程式
eq1_input = input("請輸入第一條方程式 (例如 a + 1 = 6): ")
eq2_input = input("請輸入第二條方程式 (例如 a + b = 10): ")

# 將用戶輸入的字符串轉換為符號方程式
eq1 = sp.sympify(eq1_input.replace("=", "-(") + ")")
eq2 = sp.sympify(eq2_input.replace("=", "-(") + ")")

# 解方程式
solution = sp.solve((eq1, eq2), (a, b))

# 輸出解
print("解為:", solution)
