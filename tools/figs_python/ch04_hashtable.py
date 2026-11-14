from common import *
fig, ax = canvas(8, 4.6)
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2)
ax.text(0.2, 5.9, "A tiny hash table with 8 slots (slot = hash(key) % 8)", fontsize=11, fontweight="bold")
keys = {0: [("10", "'ann'")], 2: [("18", "'bo'"), ("2", "'cy'")], 5: [("13", "'di'")], 7: [("7", "'ed'")]}
for slot in range(8):
    y = 5.2 - slot * 0.62
    box(ax, 0.3, y, 0.9, 0.5, str(slot), GREY, fs=10)
    if slot in keys:
        x = 1.6
        for k, v in keys[slot]:
            box(ax, x, y, 2.2, 0.5, f"key {k} : {v}", BLUE if len(keys[slot]) == 1 else ORANGE, fs=9.5)
            x += 2.5
ax.text(5.0, 1.5, "Slot 2 holds two keys:\n18 % 8 = 2 and 2 % 8 = 2.\nThis is a collision.\nPython probes for another\nfree slot, then compares\nkeys with ==.", fontsize=10.5, va="center", color=ORANGE)
save(fig, "ch04_hashtable.png")
