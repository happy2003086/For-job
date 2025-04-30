import numpy as np
import matplotlib.pyplot as plt

# 假設嘅年份
hong_kong_years = np.array([1961, 2021])
hong_kong_ages = np.array([23, 46])

uk_years = np.array([2001, 2022])
uk_ages = np.array([38, 40])

# 插值生成每一年的年齡變化
hong_kong_interpolated_years = np.arange(1961, 2022)
hong_kong_interpolated_ages = np.interp(hong_kong_interpolated_years, hong_kong_years, hong_kong_ages)

# 計算英國年均增長速度
uk_annual_growth_rate = (uk_ages[1] - uk_ages[0]) / (uk_years[1] - uk_years[0])

# 假設這個年均增長速度持續
uk_extended_years = np.arange(2001, 2031)  # 擴展到2030年
uk_extended_ages = uk_ages[0] + uk_annual_growth_rate * (uk_extended_years - uk_years[0])

# 可視化數據
plt.figure(figsize=(10, 6))

# 香港人口老化速度
plt.plot(hong_kong_interpolated_years, hong_kong_interpolated_ages, label='香港', color='blue', linewidth=2)

# 擴展後嘅英國人口老化速度
plt.plot(uk_extended_years, uk_extended_ages, label='英國 (生育率假設不變)', color='green', linestyle='dashed', linewidth=2)

# 標籤同標題
plt.title('香港與英國人口老化速度比較（英國生育率假設不變）', fontsize=16)
plt.xlabel('年份', fontsize=14)
plt.ylabel('中位數年齡', fontsize=14)

# 顯示圖例
plt.legend()

# 顯示圖表
plt.grid(True)
plt.show()
