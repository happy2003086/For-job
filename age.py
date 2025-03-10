import numpy as np

def population_decline_with_death(initial_population, annual_decrease_rate, start_year, end_year, life_expectancy):
  """
  模拟人口逐年下降，考虑固定平均寿命

  Args:
    initial_population: 初始人口
    annual_decrease_rate: 年降幅
    start_year: 开始年份
    end_year: 结束年份
    life_expectancy: 平均壽命

  Returns:
    一个列表，其中每个元素表示对应年份的人口数
  """

  population = initial_population
  results = []
  for year in range(start_year, end_year + 1):
    # 简单死亡率计算：假设70岁以上的人全部死亡
    population -= np.sum(np.where(np.arange(start_year, year + 1) >= year - life_expectancy + start_year, 1, 0))
    # 其他因素导致的人口减少
    population *= (1 - annual_decrease_rate)
    results.append(population)
  return results

# 设置参数
initial_population = 7500000
annual_decrease_rate = 0.01
start_year = 2020
end_year = 2100
life_expectancy = 70

# 计算并输出结果
population_data = population_decline_with_death(initial_population, annual_decrease_rate, start_year, end_year, life_expectancy)

for year, population in zip(range(start_year, end_year + 1), population_data):
  print(f"在 {year} 年，人口为 {population:.2f} 万")