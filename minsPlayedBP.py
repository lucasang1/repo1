import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv("forwards.csv")
y = "Minutes played"

# colour-coding by club
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

# use small jitter to separate each plot
np.random.seed(42) 
df["jitter"] = np.random.normal(loc = 0, scale = 0.04, size = len(df))
max_jit = df["jitter"].abs().max()
box_thickness = max_jit * 2.5


# 1) add the box (horizontal)
fig = go.Figure()
fig.add_trace(go.Box(
    x = df[y],
    y = [0] * len(df),
    orientation = 'h',
    boxpoints = False,
    fillcolor = 'gray',
    opacity=0.5,
    width = box_thickness,
    line=dict(color='white'),
    marker=dict(color='gray'),
    hoverinfo='skip',
    showlegend=False
))

# 2) overlay each club as its own scatter trace
for club, color in club_colors.items():
    club_df = df[df["Club"] == club]
    fig.add_trace(go.Scatter(
        x = club_df[y],
        y = club_df["jitter"],
        mode = 'markers',
        name = club,
        marker = dict(size = 10, color = color),
        hovertemplate=(
            "<b>%{text}</b><br>"
            + club + "<br>" + "<br>" + 
            "<extra>%{x}mins</extra>"
        ),
        text=club_df["Player"]
    ))

# layout tweaks
fig.update_layout(
    title = "Distribution of Minutes Played (by SPL Forwards)",
    template = "plotly_dark",
    xaxis = dict(title="Minutes Played", range=[0, df[y].max() * 1.02]),
    yaxis=dict(title="", range=[-max_jit*3, max_jit*3], showticklabels=False),
    margin = dict(l = 60, r = 40, t = 80, b = 60),
    legend = dict(title="Club", font = dict(size = 10))
)

fig.show()
fig.write_html("minsPlayedBP_interactive.html")
