import math

def heron_area(a, b, c):
    # 計算半周長
    s = (a + b + c) / 2
    # 使用海龍公式計算面積
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

# 讓使用者輸入三邊長
a = float(input("請輸入第一條邊長 a: "))
b = float(input("請輸入第二條邊長 b: "))
c = float(input("請輸入第三條邊長 c: "))

# 計算並顯示面積
area = heron_area(a, b, c)
print(f"三角形的面積是: {area}")
