import numpy as np

# Constants
g = 9.81  # acceleration due to gravity in m/s²

# Get the height from the user
h = float(input("Enter the height from which the egg is dropped (in meters): "))

# Calculate the time it takes to fall
t = np.sqrt(2 * h / g)

# Calculate the final velocity
v = g * t

print(f"Time to fall: {t:.2f} seconds")
print(f"Speed when hitting the ground: {v:.2f} m/s")
