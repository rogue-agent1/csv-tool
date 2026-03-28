#!/usr/bin/env python3
"""CSV toolkit — read, filter, sort, stats, convert."""
import sys, csv, json, io

def read_csv(path):
    with open(path) as f: return list(csv.DictReader(f))

def stats(rows, col):
    vals = []
    for r in rows:
        try: vals.append(float(r[col]))
        except (ValueError, KeyError): pass
    if not vals: return {"error": "no numeric values"}
    return {"count": len(vals), "min": min(vals), "max": max(vals),
            "sum": sum(vals), "mean": sum(vals)/len(vals)}

def filter_rows(rows, col, op, val):
    result = []
    for r in rows:
        v = r.get(col, "")
        try: v, val2 = float(v), float(val)
        except ValueError: val2 = val
        if op == "==" and v == val2: result.append(r)
        elif op == "!=" and v != val2: result.append(r)
        elif op == ">" and isinstance(v,(int,float)) and v > val2: result.append(r)
        elif op == "<" and isinstance(v,(int,float)) and v < val2: result.append(r)
        elif op == "contains" and val.lower() in str(v).lower(): result.append(r)
    return result

def cli():
    if len(sys.argv) < 3: print("Usage: csv_tool <file> <cmd> [args]"); print("  head|stats COL|filter COL OP VAL|json|cols"); sys.exit(1)
    path, cmd = sys.argv[1], sys.argv[2]
    rows = read_csv(path)
    if cmd == "head":
        n = int(sys.argv[3]) if len(sys.argv)>3 else 5
        for r in rows[:n]: print(r)
    elif cmd == "cols": print(list(rows[0].keys()) if rows else "empty")
    elif cmd == "stats": print(json.dumps(stats(rows, sys.argv[3]), indent=2))
    elif cmd == "json": print(json.dumps(rows, indent=2))
    elif cmd == "filter":
        r = filter_rows(rows, sys.argv[3], sys.argv[4], sys.argv[5])
        print(f"{len(r)} rows match"); [print(row) for row in r[:10]]
    elif cmd == "count": print(f"{len(rows)} rows")

if __name__ == "__main__": cli()
