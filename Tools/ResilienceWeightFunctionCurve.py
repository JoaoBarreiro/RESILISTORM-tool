import numpy as np
import matplotlib.pyplot as plt

def f(x, b):
    return (1 - x) * np.exp(-b * x)

b = 0.7

# Number of divisions (n=3 for the example)
n = 4

# Calculate the x-coordinates for the vertical lines
x_points = np.linspace(0, 1, n)

# Generate x values between 0 and 1
x = np.linspace(0, 1, 100)

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(x, f(x, b), label=f'f(x) with b={b}')

# Adding vertical lines and annotations
for x_p in x_points:
    y_p = f(x_p, b)
    plt.axvline(x=x_p, color='red', linestyle='--', linewidth = 0.8)
    
    plt.text(x_p, y_p, f'({y_p:.2f})', verticalalignment='bottom')
    # plt.text(x_p, y_p, f'({x_p:.2f}, {y_p:.2f})', verticalalignment='bottom')

# Setting the title with LaTeX-style formatting
plt.title(r'$f(x) = (1 - x)e^{-' + str(b) + 'x}$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
# plt.legend()
plt.show()
