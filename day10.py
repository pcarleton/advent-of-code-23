from util import *

input = "./day10/test2.txt"
input = "./day10/input.txt"

D = open(input).readlines()

mat = [l.strip() for l in D]

# pipe: F7JL-|

deltas = {
    'F': [(1, 0), (0, 1)],
    '7': [(-1, 0), (0, 1)],
    'J': [(0, -1), (-1, 0)],
    'L': [(0, -1), (1, 0)],
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    '.': [],
}
dc = {k: [complex(x, y) for x,y in v] for k, v in deltas.items()}

def print_delta(l):
    grid = [[(x-1, y-1) for x in range(3)] for y in range(3)]
    lets = [['*' if (x,y) in deltas[l] else ' ' for x,y in r] for r in grid]
    lets[1][1] = l

    print("\n".join("".join(r) for r in lets))

# for k in deltas:
#     print("="*10)
#     print_delta(k)

def conns(cur, let):
    return [cur + d for d in dc[let]]

def next_for_pipe(origin, cur, let):
    nxt = [p for p in conns(cur, let) if p != origin][0]
    return nxt

def mchar(i):
    return mat[int(i.imag)][int(i.real)]

def surround(origin):
    deltas = [complex(x-1, y-1) for x in range(3) for y in range(3) if (x-1,y-1) != (0, 0)]
    return [origin+d for d in deltas]

s_coord = None
for y in range(len(mat)):
    for x in range(len(mat[0])):
        # print(x, mat[y], len(mat[0]))
        if mat[y][x] == 'S':
            s_coord = complex(x, y)


first_pipes = [p for p in surround(s_coord) if s_coord in conns(p, mchar(p))]


prev = s_coord
cur = first_pipes[0]
locs = [cur]
while cur != s_coord:
    nxt = next_for_pipe(prev, cur, mchar(cur))
    prev = cur
    cur = nxt
    locs.append(cur)


print(f"part1: {len(locs) // 2}")

from collections import deque
edge_queue = deque()
edge_queue.append((0+0j))

pipes = set(locs)
outside = set()
visited = set()

while len(edge_queue) > 0:
    targ = edge_queue.popleft()
    if targ in visited:
        continue

    visited.add(targ)
    if targ in pipes:
        continue

    outside.add(targ)
    neighbors = [n for n in surround(targ) if n.real >= 0 and n.imag >= 0 and n.real < len(mat[0]) and n.imag < len(mat)]
    edge_queue.extend([n for n in neighbors if n not in visited])

# print(outside, len(outside))


locpts = {(p.real, p.imag) for p in locs}


# for k in deltas:
#     print("="*10)
#     print_delta(k)

polarities = """AAA
AF*
A*B

AAA
*7A
B*A

A*B
*JB
BBB

A*B
AL*
AAA

A*B
A|B
A*B

AAA
*-*
BBB
"""

import collections
regions = collections.defaultdict(dict)
gs = polarities.split("\n\n")
for g in gs:
    lines = g.split("\n")
    c = lines[1][1]
    alist = []
    blist = []
    # print(lines)
    for pt in [(x,y) for x in range(3) for y in range(3)]:
        x, y = pt
        cp = lines[y][x]
        pt2 = (x-1, y-1)
        if cp in ('A', 'B'):
            regions[c][pt2] = cp
            regions[c][complex(*pt2)] = cp
    
flips = """FJ-
F7-
F--
F|-
7L^
7--
7|^
JL^
J--
J|-
L-^
L|^"""

fdict = collections.defaultdict(list)
for f in flips.split("\n"):
    c1, c2, fc = f.strip()
    if fc == '^':
        fdict[c1].append(c2)
        fdict[c2].append(c1)
    
edge_pipe = locs[0]
for i in range(len(locs)):
    p = locs[i]

    ns = set(surround(p))
    reds = ns & outside

    if len(reds) > 0:
        edge_pipe = p
        edge_idx = i
        # print(reds)
        break

red_edge = 'A'
start = 0
edge_map = {edge_pipe: 'A'}

def pick_side(s, cc, nc):
    if nc in fdict[cc]:
        if s == 'A':
            return 'B'
        return 'A'
    return s

for i in range(len(locs)):
    idx = (edge_idx + i) % len(locs)
    nxtidx = (idx + 1) %len(locs)
    cur = locs[idx]
    cur_e = edge_map[cur]
    nxt = locs[nxtidx]
    cc = mchar(cur)
    c = mchar(nxt)
    nxt_e = pick_side(cur_e, cc, c)
    edge_map[nxt] = nxt_e


outpts = {(p.real, p.imag) for p in outside}

allpts = {(x, y) for x in range(len(mat[0])) for y in range(len(mat))}

cands = allpts - locpts - outpts

targ = min(cands)
targc = complex(*targ)

def in_or_out(cand, all_out, all_inside):
    ns = set(surround(cand))

    outs = ns & all_out
    if len(outs) > 0:
        return False
    
    ins = ns & all_inside
    if len(ins) > 0:
        return True
    
    for n in ns:
        if n not in pipes:
            continue
        d = n - cand
        edge_side = edge_map[n]
        
        this_side = regions[mchar(n)].get(d)
        if this_side is None:
            print(n)

        if edge_side == this_side:
            return True
    return False


print(f"neighbor: {targc + 1}, {mchar(targc+1)}, {edge_map[targc+1]}, {regions[mchar(targc+1)][complex(-1, 0)]}")

def mpt(cmpx):
    return (cmpx.real, cmpx.imag)

candsi = set(complex(*c) for c in cands)
inside = set()
for c in candsi:
    if in_or_out(c, outside, inside):
        inside.add(c)


remaining = candsi - inside
for r in remaining:
    if in_or_out(r, outside, inside):
        inside.add(r)


inpts = [mpt(p) for p in inside]

annotated = "\n".join([
    "".join( colorize(x, y, c, [(YELLOW, inpts), (GREEN, locpts), (RED, outpts), (BLUE, cands)]) for x, c in enumerate(row)        )
    for y, row in enumerate(mat)
])

print(annotated)


