import matplotlib
matplotlib.use("Agg")
import seaborn as sns

sns.set_theme(style="white", context="notebook", palette="colorblind", font_scale=1.0)
print("colorblind palette:", sns.color_palette("colorblind").as_hex()[:6])
print("default notebook font size:", sns.plotting_context("notebook")["axes.labelsize"],
      "| talk:", sns.plotting_context("talk")["axes.labelsize"],
      "| poster:", sns.plotting_context("poster")["axes.labelsize"])
print("styles:", ["white", "whitegrid", "dark", "darkgrid", "ticks"])
print("blues (5 steps):", sns.color_palette("Blues", 5).as_hex())
print("diverging:", sns.diverging_palette(250, 30, n=5).as_hex())
