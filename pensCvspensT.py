import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("forwards.csv")
df_filtered = df[df["Penalties taken"] > 0]
x, y = "Penalties taken", "Penalty Goal Conversion %"

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

# create scatterplot
df["LocalYN"] = df["Is Local"].map({"Y": "Local", "N": "Foreigner"})
fig = px.scatter(
    df, x = x, y = y,
    color = "Club",
    color_discrete_map = club_colors,
    hover_name = "Player",
    hover_data = {x, y, "Club", "LocalYN"},
    custom_data=["Club", "LocalYN"],  
    title = "Penalty Conversion % vs Penalties Taken",
)

# update hover information and trace size
fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>" +
        "%{customdata[0]}<br>" +
        "<extra>Penalty Conversion: %{y}%<br>"
        "Penalties Taken: %{x}<br>" +
        "%{customdata[1]}</extra>"
    ),
    marker = dict(size = 10)
)

# plot 90th percentile lines and shading upper square
x90 = df[x].quantile(0.9)
y90 = df[y].quantile(0.9)
fig.add_vline(
    x = x90,
    line_dash = "dash",
    line_color = "gold",
    line_width = 1,
    annotation_text = f"90th Percentile ({x90:.0f} Penalties)",
    annotation_position = "top left",
    annotation_font_color = "gold"
)
fig.add_hline(
    y = y90,
    line_dash = "dash",
    line_color = "gold",
    line_width = 1,
    annotation_text = f"90th Percentile ({y90:.0f}%)",
    annotation_position = "bottom right",
    annotation_font_color = "gold"
)
fig.add_shape(
    type = "rect",
    x0 = x90, x1 = df[x].max() * 1.02,
    y0 = y90, y1 = df[y].max() * 1.1,
    fillcolor = "gold",
    opacity = 0.2,
    layer = "below",
    line_width = 0
)

# layout adjustment
fig.update_layout(
    template = "plotly_dark",
    xaxis = dict(range = [0, df[x].max() * 1.02], title = "Penalties Taken"),
    yaxis = dict(range = [-1, df[y].max() * 1.1], title = "Penalty Conversion %"),
    margin = dict(l = 60, r = 40, t = 80, b = 60),
    legend = dict(font = dict(size = 10))
    ) 

fig.show()
fig.write_html("pensCvspensT_interactive.html")