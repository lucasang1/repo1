import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
from matplotlib.lines import Line2D

df = pd.read_csv("forwards.csv")
y = "Minutes played"

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
ax.boxplot(df[y], vert = False, widths = 0.3, patch_artist = True,
           boxprops = dict(facecolor='gray', alpha=0.5, edgecolor='white'),
           medianprops = dict(color='gold', linewidth=2)
)

texts = []
y_upper = df[y].quantile(0)
local_fill_dic = {"Y": 1.0, "N": 0.0}
for _, row in df.iterrows():
    # horizontal jitter around x = 1
    y_jitter = np.random.normal(loc = 1, scale = 0.06)
    club = row["Club"]
    col = club_colors.get(club, "white")

    sc = ax.scatter(
        row[y], y_jitter,
        s = 100, marker = "o",
        edgecolors = col,
        facecolors = col if row["Is Local"] == "Y" else "none",
        alpha = 0.8, linewidth = 1.5,
        zorder=2
    )

    if row[y] >= y_upper:
        texts.append(
            ax.text(
                row[y], y_jitter,
                row["Player"],
                fontsize = 9,
                ha = "left", va = "center",
                zorder = 4
            )
        )

# adjust overlapping labels
adjust_text(
    texts, ax = ax,
    arrowprops = dict(arrowstyle = '-', color = 'white', lw = 0.5),
    expand_text = (1.2, 1.2), expand_points = (1.2, 1.2),
    force_text = .5, force_explode = 0.5
    )

# axes and title labels
ax.set_title("Distribution of Minutes Played (by SPL Forwards)")
ax.set_xlabel("Minutes Played")
ax.set_yticks([])

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
    handles = legend, loc = "upper right", frameon = True, 
    facecolor='#222', edgecolor = "w", fontsize = 9)

plt.tight_layout()
plt.show()
