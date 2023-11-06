import matplotlib.pyplot as plt

# Data for the cumulative series
cumulative_data = [0.5, 0.4, 0.1]

# Calculate the cumulative values
cumulative_values = [sum(cumulative_data[:i + 1]) for i in range(len(cumulative_data))]

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Create the cumulative horizontal bar chart
ax.barh([1], cumulative_values, color='blue', alpha=0.7, height=0.6)

# Customize the appearance of the plot
ax.set_yticks([1])
ax.set_yticklabels(['Cumulative Values'])
ax.set_xlabel('Values')
ax.set_title('Cumulative Horizontal Bar Chart')

# Show the plot
plt.show()
