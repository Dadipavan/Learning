import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
fig, ax = canvas(9.5, 5.2)
ax.text(1, 49, "Separated compute and storage: many clusters, one copy of the data", fontsize=10.5, color=BLUE, weight="bold")
box(ax, 4, 38, 24, 7, "Dashboards\nsmall cluster, always on", BLUE, fs=9)
box(ax, 38, 38, 24, 7, "Nightly ETL (dbt)\nlarge cluster, 2 h a night", ORANGE, fs=9)
box(ax, 72, 38, 24, 7, "Data science\nmedium, on demand", PURPLE, fs=9)
box(ax, 20, 22, 60, 7, "Metadata service: table layout, min/max stats, access rules", TEAL, fs=9.5)
box(ax, 10, 5, 80, 9, "Shared storage: columnar files in object storage\none copy, billed per TB per month", GREY, fs=10)
for x in (16, 50, 84):
    arrow(ax, x, 37.6, min(max(x, 25), 75), 29.8, GREY)
arrow(ax, 50, 21.6, 50, 14.4, GREY)
ax.text(52, 31.5, "scale each cluster separately;\npay only while it runs", fontsize=8, color=ORANGE)
ax.text(70, 18, "a cluster never owns the data,\nso it can be resized or paused", fontsize=8.5, color=ORANGE)
fig.savefig("de_wh_separation.png", dpi=110, bbox_inches="tight")
