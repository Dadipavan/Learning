#!/bin/sh
# Copy chapter next to the src dir so the checker's image path resolves, then run it.
cd /Users/c2487352/Personal/Career/final
cp study/ml/$1.html tools/figs_ml/src/_chk_$1.html
python3 tools/check_fragment.py tools/figs_ml/src/_chk_$1.html --loose --doc ml --run | tail -8
rm tools/figs_ml/src/_chk_$1.html
