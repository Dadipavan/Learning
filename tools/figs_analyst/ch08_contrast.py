import matplotlib
matplotlib.use("Agg")
import numpy as np
from matplotlib.colors import to_rgb

def luminance(hex_colour):
    c = np.array(to_rgb(hex_colour))
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(c @ np.array([0.2126, 0.7152, 0.0722]))

def contrast(a, b="#ffffff"):
    la, lb = sorted([luminance(a), luminance(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

for name, h in [("light grey (context marks)", "#9a9a9a"), ("mid grey (text)", "#666666"), ("dark grey (text)", "#333333"),
                ("blue", "#2b4fd6"), ("orange", "#b84a22"), ("teal", "#357a70"), ("red", "#aa2d26"), ("purple", "#6a2fd0")]:
    ratio = contrast(h)
    verdict = "text ok" if ratio >= 4.5 else ("graphics ok" if ratio >= 3 else "too faint")
    print(f"{name:<27}{h}  {ratio:5.2f}:1  {verdict}")
