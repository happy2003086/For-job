# 假設初始人口係750萬
initial_population = 7500000

# 假設每年人口減少0.9%（反映人口流失）
annual_decline_rate = 0.009

# 模擬100年後嘅人口
years = 100
population = initial_population

# 從2020年開始計算
start_year = 2020

for year in range(1, years + 1):
    population *= (1 - annual_decline_rate)
    
    # 每年輸出一下人口並顯示年份
    print(f"{int(population)} ({start_year + year - 1}年)")
