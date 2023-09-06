import matplotlib.pyplot as plt

# Sample data
categories = ["Obj1: Cool!", "Obj2: Awesome!", "Obj3: Amazing!", "Obj4: Fantastic!"]
values = [10, 20, 15, 30]

# Create the plot
plt.barh(range(len(categories)), values, tick_label=categories)

# Function to display the label on mouseover
def on_hover(event):
    if event.inaxes == plt.gca() and event.xdata is not None and event.ydata is not None:
        y_ticks = plt.gca().get_yticks()
        y_tick_labels = plt.gca().get_yticklabels()

        y_coord = event.y
        y_index = int(y_coord + 0.5)  # Round to the nearest integer
        if y_index >= 0 and y_index < len(y_ticks):
            x_coord = event.x
            xmin, xmax = plt.gca().get_xlim()
            ymin, ymax = plt.gca().get_ylim()
            if x_coord >= xmin and x_coord <= xmax and y_coord >= ymin and y_coord <= ymax:
                category = y_tick_labels[y_index].get_text()
                plt.gca().annotate(category, xy=(0, y_ticks[y_index]), xytext=(-20, 0),
                                   xycoords=('axes fraction', 'data'), textcoords='offset points',
                                   ha='right', va='center', fontsize=10, fontweight='bold', color='blue')
                plt.draw()
        else:
            plt.gca().get_children()[-1].remove()
            plt.draw()

# Connect the on_hover function to the MotionNotify event
plt.gcf().canvas.mpl_connect('motion_notify_event', on_hover)

# Show the plot
plt.tight_layout()
plt.show()
