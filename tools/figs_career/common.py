import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE="#2b4fd6"; ORANGE="#b84a22"; TEAL="#357a70"; RED="#aa2d26"; PURPLE="#6a2fd0"; GREY="#999999"
def clean(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
