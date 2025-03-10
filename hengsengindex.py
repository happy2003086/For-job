import yfinance as yf
import matplotlib.pyplot as plt

# 下載恆生指數數據
data = yf.download('^HSI', start='1997-07-01', end='2025-03-01', auto_adjust=True)

# 顯示資料的頭幾行
print(data.head())

# 計算最高點和最低點
max_price = data['Close'].max()  # 最高價
min_price = data['Close'].min()  # 最低價

# 確保 max_price 和 min_price 是數字
max_price = max_price.item()
min_price = min_price.item()

# 計算最大跌幅
max_drop = (max_price - min_price) / max_price * 100

# 顯示最大下跌幅度
print(f"恆生指數最大下跌幅度: {max_drop:.2f}%")

# 繪製圖表
plt.figure(figsize=(10,6))
plt.plot(data['Close'], label='恆生指數收盤價')
plt.axhline(max_price, color='red', linestyle='--', label=f'最高價: {max_price:.2f}')
plt.axhline(min_price, color='blue', linestyle='--', label=f'最低價: {min_price:.2f}')
plt.title("恆生指數走勢圖")
plt.xlabel("日期")
plt.ylabel("價格")
plt.legend()
plt.grid(True)
plt.show()
