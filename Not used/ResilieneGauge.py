import matplotlib.pyplot as plt
import math

colors = ["#1a9850", "#a6d96a", "#ffffbf", "#fdae61", "#d73027"]

label_values = [1, 0.9, 0.75, 0.55, 0.3, 0]

bar_proportion = [0.1, 0.15, 0.2, 0.25, 0.3]

x_widths_radians = [3.14*value for value in bar_proportion]

#print(x_widths_radians)

rad_coor = []
for index, val in enumerate(bar_proportion):
    if index == 0:
        rad_coor.append(index)
    else:
        rad_coor.append(rad_coor[index-1] + x_widths_radians[index-1])
    

fig = plt.figure(figsize=(5,5))

ax = fig.add_subplot(projection = "polar")

ax.bar(x = rad_coor, width = x_widths_radians, height = 0.5, bottom = 2, color = colors,
       linewidth = 0, edgecolor = "white",
       align = "edge")


# for loc, val in zip(rad_coor, label_values):
#     plt.annotate(val, xy=(loc, 2.25), ha = "center", va = "center")

Res = 0.67

plt.annotate(text = Res, xytext =(0,0), xy =((1 - Res)* 3.14, 2.25),
             arrowprops = dict(arrowstyle = "wedge", color = "black", shrinkA=0),
             bbox=dict(boxstyle = "circle", facecolor = "black", linewidth = 2.0),
             fontsize = 15, color = "white", ha = "center"
            )

#ax.set_axis_off()


plt.show()