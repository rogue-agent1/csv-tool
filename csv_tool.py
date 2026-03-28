#!/usr/bin/env python3
"""CSV toolkit — read, filter, sort, stats, convert."""
import sys, csv, json
def cli():
    if len(sys.argv)<3: print("Usage: csv_tool <file> head|cols|count|json|stats COL"); sys.exit(1)
    with open(sys.argv[1]) as f: rows=list(csv.DictReader(f))
    cmd=sys.argv[2]
    if cmd=="head": [print(r) for r in rows[:int(sys.argv[3]) if len(sys.argv)>3 else 5]]
    elif cmd=="cols": print(list(rows[0].keys()) if rows else [])
    elif cmd=="count": print(len(rows))
    elif cmd=="json": print(json.dumps(rows,indent=2))
    elif cmd=="stats":
        col=sys.argv[3]; vals=[float(r[col]) for r in rows if r.get(col,"").replace(".","",1).lstrip("-").isdigit()]
        print(f"  count={len(vals)} min={min(vals):.2f} max={max(vals):.2f} mean={sum(vals)/len(vals):.2f}")
if __name__ == "__main__": cli()
