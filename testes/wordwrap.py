import matplotlib.pyplot as plt
import textwrap

# Create a sample plot
objectives = ["This is a very long label", "Another long label", "Short label", "Yet another long label"]
values = [10, 20, 15, 30]

fig, ax = plt.subplots()
ax.barh(objectives, values)

# Enable word wrapping for Y-axis labels
ax.set_yticklabels([textwrap.fill(label, 15) for label in objectives])

plt.show()