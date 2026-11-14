cd /Users/c2487352/Personal/Career/final/tools/figs_sql/gen03d
python3 -c "
import sys
sys.argv=['x','p0.py']+sys.argv[1:]
exec(open('run.py').read())" $(ls p[1-9].py)
