def pick_theorem(I, B):
    """根據皮克定理計算格點多邊形的面積"""
    return I + B / 2 - 1

# 測試範例
I = int(input("請輸入內部的格點數量 I: "))
B = int(input("請輸入邊界上的格點數量 B: "))

area = pick_theorem(I, B)
print(f"該多邊形的面積為: {area}")
