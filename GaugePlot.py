import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties

def create_circular_bar(value):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"aspect": "equal"})

    # Normalize the value between 0 and 1
    norm_value = (value - 0) / (1 - 0)

    # Create a circular bar with cmap color for filled part and lightgrey for remaining part
    cmap = cm.get_cmap('RdYlGn')
    filled_color = cmap(norm_value)
    empty_color = 'lightgrey'
    
    # Create the remaining part of the circular bar
    wedge_empty = patches.Wedge((0, 0), 1, 360 * norm_value, 360, width=0.4, facecolor=empty_color, alpha=0.2, edgecolor='black')
    ax.add_patch(wedge_empty)
    
    # Create the filled part of the circular bar
    wedge_filled = patches.Wedge((0, 0), 1, 0, 360 * norm_value, width=0.4, facecolor=filled_color, edgecolor='black')
    ax.add_patch(wedge_filled)

    # Display the value in the center
    font = FontProperties(family='Segoe UI', weight='bold')
    ax.text(0, 0, f"{value}", fontsize=60, ha='center', va='center', fontproperties = font)

    # Set the axis limits and remove the axis labels
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis("off")

    # Show the plot
    plt.show()

# Example usage
value = 0.75
create_circular_bar(value)
