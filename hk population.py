# 初始人口
population_2019 = 7440000
# 每年減少嘅人口數量
annual_decrease = 40000
# 預測未來 10 年嘅人口
years = 100
populations = [population_2019]
for i in range(1, years + 1):
    new_population = populations[-1] - annual_decrease
    populations.append(new_population)

# 顯示未來每年嘅人口
for year, population in enumerate(populations, start=2019):
    print(f"{year} 年人口預測: {population} 人")
