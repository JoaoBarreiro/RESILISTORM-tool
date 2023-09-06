import pandas as pd
import matplotlib.pyplot as plt

# Define the table data
data = {
    'I1': [0.9, 0.7, 0.92],
    'I2': [0.92, 0.75, 0.98],
    'I3': [0.8, 0.75, 0.9]
}

# Create a DataFrame from the table data
df = pd.DataFrame(data, index=['Atual', 'Futuro BAU', 'Futuro ST01'])

# Reset the index to make the row names a regular column
df = df.reset_index()

# Melt the DataFrame to transform the table into a long format
df_melted = pd.melt(df, id_vars='index', var_name='Category', value_name='Value')

# Rename the columns
df_melted.columns = ['Series', 'Category', 'Value']

# Create the scatter plot
plt.scatter(df_melted['Value'], df_melted['Category'], c='b', marker='o')

# Set the x-axis label
plt.xlabel('Value')

# Show the plot
plt.show()
