import matplotlib
matplotlib.use("Agg")
import json

figure = {
    "data": [{"type": "bar", "x": ["Delhi", "Mumbai", "Pune"], "y": [3298, 3047, 2995],
              "marker": {"color": ["#2b4fd6", "#9a9a9a", "#9a9a9a"]},
              "hovertemplate": "%{x}: Rs %{y:,.0f}<extra></extra>"}],
    "layout": {"title": {"text": "Delhi sold the most: Rs 3,298 of Rs 9,340"},
               "yaxis": {"title": {"text": "Sales (Rs)"}, "range": [0, 3800]},
               "template": "plotly_white"},
}
print(json.dumps(figure["data"][0]))
print(json.dumps(figure["layout"]))
print("traces:", len(figure["data"]), "| trace type:", figure["data"][0]["type"],
      "| layout keys:", sorted(figure["layout"]))
