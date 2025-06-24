import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.lines import Line2D

df = pd.read_csv("forwards.csv")

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
x, y = "Total shots", "Non-Penalty Goal Conversion %"
ax.set_xlim(0, 180)
ax.set_ylim(-1, 52)

# plot 90th percentile lines
x90 = df[x].quantile(0.9)
y90 = df[y].quantile(0.9)
ax.axvline(x90, color = "gold", linestyle = "--", lw = 1, zorder = 1)
ax.axhline(y90, color = "gold", linestyle = "--", lw = 1, zorder = 1)
ax.axvspan(xmin = x90, xmax = ax.get_xlim()[1], 
           ymin = (y90 - ax.get_ylim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0]), 
           ymax = 1, color='gold', alpha=0.2)

# plot points and collect labels
texts = []
x_upper = df[x].quantile(0.45)
y_upper = df[y].quantile(0.45)
for _, row in df.iterrows():
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
                fontsize = 9,
                ha = "right", va = "bottom",
                zorder = 4
            )       
        )

adjust_text(
    texts, ax = ax,
    arrowprops = dict(arrowstyle = '-', color = 'white', lw = 0.5),
    expand_text = (1.2, 1.2), expand_points = (1.2, 1.2),
    force_text = 2.5, force_explode = 3.5
    )

ax.text(
    x90, ax.get_ylim()[1]*1.03, f"90th Percentile ({x90:.0f} Shots)", 
    ha="center", va="top", color="gold", fontsize=9)
ax.text(
    ax.get_xlim()[1]*1.02, y90, f"90th Percentile ({y90:.0f}%)", 
    ha="right", va="center", color="gold", fontsize=9, rotation=90)

ax.set_title("Non-Penalty Goal Conversion % vs Total Shots (by SPL Forwards)", fontsize = 14, pad = 20)
ax.set_xlabel("Total Shots", fontsize = 11)
ax.set_ylabel("Non-Penalty Goal Conversion %", fontsize = 11)
plt.show()
