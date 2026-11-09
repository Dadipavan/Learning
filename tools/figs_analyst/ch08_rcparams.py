import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rc_context
from matplotlib.colors import to_hex

print("default figure size:", plt.rcParams["figure.figsize"], "| dpi:", plt.rcParams["figure.dpi"],
      "| font size:", plt.rcParams["font.size"])
print("default top spine visible:", plt.rcParams["axes.spines.top"])
print("first 3 colours of the default cycle:", [to_hex(d["color"]) for d in plt.rcParams["axes.prop_cycle"]][:3])

house = {"figure.figsize": (8, 4.2), "figure.dpi": 110, "font.size": 12, "axes.titlesize": 14,
         "axes.titleweight": "bold", "axes.titlelocation": "left",
         "axes.spines.top": False, "axes.spines.right": False}
with rc_context(house):                      # temporary: restored when the block ends
    print("inside context  :", plt.rcParams["figure.figsize"], plt.rcParams["axes.titlelocation"])
print("after context   :", plt.rcParams["figure.figsize"], plt.rcParams["axes.titlelocation"])
