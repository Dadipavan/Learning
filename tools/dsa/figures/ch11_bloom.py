import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch05_common import *

fig, ax = canvas(16, 8.4)
txt(ax, 8, 7.9, "Bloom filter: 16 bits, 3 hash functions (made-up positions)", BLUE, 15, weight="bold")
bits = [0] * 16
for i in (2, 7, 11, 5, 14):
    bits[i] = 1
for i, b in enumerate(bits):
    box(ax, 0.4 + i * 0.95, 4.2, 0.9, 1.0, str(b), TEAL if b else GREY, fc="#e3f1ee" if b else "white", fs=14)
    txt(ax, 0.85 + i * 0.95, 3.8, str(i), GREY, 10)


def px(i):
    return 0.85 + i * 0.95


txt(ax, 4.0, 6.9, "add 'cat': sets bits 2, 7, 11", BLUE, 13)
txt(ax, 11.5, 6.9, "add 'dog': sets bits 5, 7, 14", BLUE, 13)
txt(ax, 3.6, 1.3, "ask 'emu': bits 2, 5, 11 are all 1\nanswer: maybe (a false positive)", RED, 13)
txt(ax, 11.8, 1.3, "ask 'owl': bits 3, 7, 9\nbit 3 is 0: definitely not present", TEAL, 13)
for i in (2, 5, 11):
    arrow(ax, (px(i), 2.3), (px(i), 3.55), RED, 1.8)
for i in (3, 7, 9):
    arrow(ax, (px(i), 2.3), (px(i), 3.55), TEAL, 1.8)
save(fig, "dsa11_bloom.png")
