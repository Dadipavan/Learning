from common import *
fig, ax = canvas(8, 4.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 6)
layers = [("Presentation: routes, CLI, request and response models", BLUE), ("Service layer: business rules, transactions", ORANGE),
          ("Repository layer: SQL and storage details", TEAL), ("Database / files / external APIs", GREY)]
for i, (t, c) in enumerate(layers):
    box(ax, 0.3, 4.6 - i * 1.3, 6.6, 1.0, t, c, fs=10)
    if i < 3: arrow(ax, 3.6, 4.6 - i * 1.3, 3.6, 4.6 - i * 1.3 - 0.3, GREY)
ax.text(7.2, 3.0, "Rule: each layer\ncalls only the layer\nbelow it.\n\nTests swap the\nbottom layers for\nfakes.", fontsize=10.5, va="center", color=GREY)
save(fig, "ch13_layers.png")
