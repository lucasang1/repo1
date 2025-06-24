import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.lines import Line2D

df = pd.read_csv("forwards.csv")
df_filtered = df[df["Penalties taken"] > 0]

# colour-coding by Club
club_colors = {
    "Brunei DPMM": "brown",
    "Balestier Khalsa": "red",
    "Young Lions": "deeppink",
    "Tampines Rovers": "gold",
    "Geylang International": "lime",
    "Hougang United": "orange",
    "Albirex Niigata (S)": "white",
    "Lion City Sailors": "deepskyblue",
    "Tanjong Pagar United": "magenta",
}

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(13, 8.5))
x, y = "Penalties taken", "Penalty Goal Conversion %"
ax.set_xlim(0, 8.1)
ax.set_ylim(-1, 101)

# plot 90th percentile lines
x90 = df_filtered[x].quantile(0.9)
y90 = df_filtered[y].quantile(0.9)
ax.axvline(x90, color = "gold", linestyle = "--", lw = 1, zorder = 1)
ax.axhline(y90, color = "gold", linestyle = "--", lw = 1, zorder = 1)
ax.axvspan(xmin = x90, xmax = ax.get_xlim()[1], 
           ymin = (y90 - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0]), 
           ymax = 1, color='gold', alpha=0.2)

# plot points and collect labels
texts = []
x_upper = df_filtered[x].quantile(0.) # not used
y_upper = df_filtered[y].quantile(0.)
for _, row in df_filtered.iterrows():
    club_color = club_colors[row["Club"]]
    face_color = club_color if row["Is Local"] == "Y" else "none"
    ax.scatter(
        row[x], row[y],
        marker = 'o',
        facecolors = face_color,
        edgecolors = club_color,
        s = 80,
        alpha = 1,
        zorder = 4
    )
    if row[x] >= x_upper or row[y] >= y_upper:
        texts.append(
            ax.text(
                row[x], row[y],
                row["Player"],
                fontsize = 10,
                ha = "right", va = "top",
                zorder = 4
            )       
        )

# adjust overlaps
adjust_text(
    texts, ax = ax,
    arrowprops = dict(arrowstyle = '-', color = 'white', lw = 0.5),
    )

# labelling percentile lines
ax.text(
    x90, ax.get_ylim()[1]*1.02, f"90th Percentile ({x90:.0f} Shots)", 
    ha="center", va="top", color="gold", fontsize=9)
ax.text(
    ax.get_xlim()[1]*1.015, y90, f"90th Percentile ({y90:.0f}%)", 
    ha="right", va="top", color="gold", fontsize=9, rotation=90)

# legend for club and local/foreign 
legend = []

for club, color in club_colors.items():
    legend.append(Line2D(
        [0], [0], marker = "o", color = "w",
        markerfacecolor = color, markersize = 8, label = club
        ))
    
legend.append(Line2D(
    [0], [0], marker = "o", color = "w", markerfacecolor = "w",
    markersize = 8, label = "Local", linestyle = ""
    ))

legend.append(Line2D(
    [0], [0], marker = "o", color = "w", markerfacecolor = "none",
    markersize = 8, label = "Foreigner", linestyle = ""
    ))

ax.legend(
    handles = legend, loc = "lower right", frameon = True, 
    facecolor='#222', edgecolor = "w", fontsize = 9)

ax.set_title("Penalty Conversion % vs Penalties Taken", fontsize = 14)
ax.set_xlabel("Penalties Taken", fontsize = 11)
ax.set_ylabel("Penalty Conversion %", fontsize = 11)
plt.tight_layout()
plt.show()
