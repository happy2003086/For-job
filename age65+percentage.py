import matplotlib.pyplot as plt
import numpy as np

# Set Chinese font
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Or use another font that supports Chinese
plt.rcParams['axes.unicode_minus'] = False

# Define the range of years (1950-2070, a total of 121 years)
years = np.arange(1950, 2071)

# Proportion of elderly population in Hong Kong (adjusted hypothetical data)
hong_kong_aging = np.concatenate((
    np.linspace(0.05, 0.12, 71),  # 1950-2020 (71 years)
    np.linspace(0.12, 0.45, 50)   # 2021-2070 (50 years)
))  # Total 71+50=121 data points

# Proportion of elderly population in the UK (adjusted hypothetical data)
uk_aging = np.concatenate((
    np.linspace(0.10, 0.18, 71),  # 1950-2020 (71 years)
    np.linspace(0.18, 0.30, 50)   # 2021-2070 (50 years)
))  # Total 71+50=121 data points

# Create the figure
plt.figure(figsize=(12, 7))

# Plot Hong Kong's elderly population proportion
plt.plot(years, hong_kong_aging, label='Hong Kong (65+)', color='#1f77b4', linewidth=3, marker='o', markevery=20)

# Plot the UK's elderly population proportion
plt.plot(years, uk_aging, label='UK (65+)', color='#ff7f0e', linewidth=3, marker='s', markevery=20)

# Add title and axis labels
plt.title('Comparison of Elderly (65+) Population Proportions\nHong Kong vs UK (1950-2070)', 
          fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Proportion of Population Aged 65+', fontsize=14)

# Set grid and ticks
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(np.arange(1950, 2071, 10), rotation=45)
plt.yticks(np.arange(0, 0.51, 0.05))
plt.ylim(0, 0.5)  # Set appropriate y-axis limits

# Add annotations for key years
plt.annotate('Accelerated aging in HK', xy=(2020, 0.12), xytext=(2030, 0.25),
             arrowprops=dict(arrowstyle='->'), fontsize=12,
             bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
plt.annotate('Gradual aging in UK', xy=(2050, 0.22), xytext=(2060, 0.1),
             arrowprops=dict(arrowstyle='->'), fontsize=12,
             bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))

# Add important milestones
plt.axvline(x=2020, color='gray', linestyle='--', alpha=0.5)
plt.text(2020, 0.52, '2020', ha='center', va='bottom', color='gray')

# Display the legend
plt.legend(fontsize=12, loc='upper left')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()