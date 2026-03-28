#!/usr/bin/env python3
"""csv_tool - CSV manipulation without csv module."""
import sys,json
def parse_csv(text,delim=",",quote='"'):
    rows=[];row=[];field="";in_q=False
    for c in text:
        if in_q:
            if c==quote:in_q=False
            else:field+=c
        elif c==quote:in_q=True
        elif c==delim:row.append(field);field=""
        elif c=="\n":row.append(field);rows.append(row);row=[];field=""
        else:field+=c
    if field or row:row.append(field);rows.append(row)
    return[r for r in rows if any(f.strip() for f in r)]
def to_csv(rows,delim=","):
    lines=[]
    for row in rows:
        fields=[]
        for f in row:
            f=str(f)
            if delim in f or '"' in f or "\n" in f:f='"'+f.replace('"','""')+'"'
            fields.append(f)
        lines.append(delim.join(fields))
    return"\n".join(lines)
def to_json(rows):
    if len(rows)<2:return rows
    headers=rows[0];return[dict(zip(headers,row)) for row in rows[1:]]
if __name__=="__main__":
    if len(sys.argv)<2:print("Usage: csv_tool.py <parse|json|stats|head> file");sys.exit(1)
    cmd=sys.argv[1];text=open(sys.argv[2]).read() if len(sys.argv)>2 else sys.stdin.read()
    rows=parse_csv(text)
    if cmd=="parse":
        for r in rows:print(" | ".join(r))
    elif cmd=="json":print(json.dumps(to_json(rows),indent=2))
    elif cmd=="head":
        for r in rows[:int(sys.argv[3]) if len(sys.argv)>3 else 10]:print(" | ".join(r))
    elif cmd=="stats":print(f"Rows: {len(rows)}, Cols: {max(len(r) for r in rows)}")
