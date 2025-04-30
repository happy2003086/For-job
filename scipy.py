import numpy as np
import matplotlib.pyplot as plt

# 初始條件：初速度 20 m/s，角度 45 度
v0, angle = 20, np.radians(45)
g = 9.81  # 重力加速度

# 時間序列
t = np.linspace(0, 2 * v0 * np.sin(angle) / g, 100)

# 計算 x 和 y 軌跡
x = v0 * np.cos(angle) * t
y = v0 * np.sin(angle) * t - 0.5 * g * t**2

# 繪製軌跡
plt.plot(x, y)
plt.xlabel("水平距離 (m)")
plt.ylabel("垂直高度 (m)")
plt.title("拋物線運動")
plt.grid()
plt.show()