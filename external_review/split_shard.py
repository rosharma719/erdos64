import sys
import gzip
import networkx as nx

inp, out3, out2, res, mod = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
opener = gzip.open if inp.endswith(".gz") else open
n3 = n2 = 0
with opener(inp, "rt") as f, open(out3, "w") as f3, open(out2, "w") as f2:
    for i, line in enumerate(f):
        if i % mod != res:
            continue
        line = line.strip()
        if not line:
            continue
        g = nx.from_graph6_bytes(line.encode())
        if nx.node_connectivity(g) >= 3:
            f3.write(line + "\n")
            n3 += 1
        else:
            f2.write(line + "\n")
            n2 += 1
        if (i // mod + 1) % 50000 == 0:
            print(f"  shard {res}/{mod}: processed {i//mod+1}, 3-connected={n3} strict2={n2}", file=sys.stderr, flush=True)
print(f"shard {res}/{mod} done: 3-connected={n3} strictly-2-connected={n2} total={n3+n2}")
