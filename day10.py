from util import *

input = "./day10/test2.txt"
input = "./day10/input.txt"
# input = "./day10/test4.txt"


D = open(input).readlines()

mat = [l.strip() for l in D]

# pipe: F7JL-|

deltas = {
    'F': [(1, 0), (0, 1)],
    '7': [(-1, 0), (0, 1)],
    'J': [(0, -1), (-1, 0)],
    'L': [(0, -1), (1, 0)],
    '|': [(0, -1), (0, 1)],
    'S': [(0, -1), (0, 1)], # dummy one, hacky
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

def mchar(mat, i):
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


first_pipes = [p for p in surround(s_coord) if s_coord in conns(p, mchar(mat, p))]


prev = s_coord
cur = first_pipes[0]
locs = [cur]
while cur != s_coord:
    nxt = next_for_pipe(prev, cur, mchar(mat, cur))
    prev = cur
    cur = nxt
    locs.append(cur)


print(f"part1: {len(locs) // 2}")

from collections import deque
pipes = set(locs)
g1 = set()
g2 = set()

def print_annot(curp, mat, pipes, g1=set()):
    annotated = "\n".join([
        "".join( icolorize(complex(x, y), c, [
            (RED, {curp}),
            (YELLOW, g1),
            (BLUE, g2),
            (GREEN, pipes),
            # (RED, outpts),
            # (BLUE, cands)
        ]) for x, c in enumerate(row)        )
        for y, row in enumerate(mat)
    ])
    print(annotated)

# print_annot(0 + 0*1j, mat, locs, g1)

def expand_pipes(mat, pipes):
    new_pipes = []
    for pipe in pipes:
        c = mchar(mat, pipe)
        ds = [(pipe*2+d) for d in dc[c]] + [pipe*2]
        new_pipes.extend(ds)

    return new_pipes


def echar(i, j, mat, np):
    if (i % 2 != 0) or (j % 2 != 0):
        cp = complex(j, i)
        # print(cp, np)
        if cp in np:
            return '*'
        return '#'
    return mat[i//2][j//2]


def expand(mat, pipes):
    new_pipes = expand_pipes(mat, pipes)
    nmat = []
    for i in range(len(mat)*2):
        nrow = []
        for j in range(len(mat[0])*2):
            nrow.append(echar(i, j, mat, new_pipes))
        nmat.append(nrow)

    return nmat, new_pipes



def flood_fill(p, pipes, mat):
    edge_queue = deque()
    edge_queue.append(p)

    pipes = set(pipes)
    outside = set()
    visited = set()

    i = 0

    while len(edge_queue) > 0:
        i += 1
        # if i > 1000:
        #     print(outside)
        #     break
        targ = edge_queue.popleft()
        if targ in visited:
            continue

        visited.add(targ)
        if targ in pipes:
            continue

        outside.add(targ)
        neighbors = [n for n in surround(targ) if n.real >= 0 and n.imag >= 0 and n.real < len(mat[0]) and n.imag < len
    (mat)]
        edge_queue.extend([n for n in neighbors if n not in visited])
    
    return outside


def test_expand():
    t1 = """...
    .F.
    ..."""

    tmat = [l.strip() for l in t1.split("\n")]
    nmat, np = expand(tmat, [1+1j])
    print_annot(0+0j, nmat, np)

    out1 = flood_fill(0+0j, np, nmat)
    print_annot(0+0j, nmat, np, out1)


# test_expand()

def main_expand(mat, pipes):
    nmat, np = expand(mat, pipes)
    out1 = flood_fill(0+0j, np, nmat)
    # print_annot(0+0j, nmat, np, out1)

    valid_out = [p for p in out1 if mchar(nmat, p) != '#']
    total = len(mat)*len(mat[0])
    print(f"out: {len(valid_out)}, pipes: {len(pipes)}, remain: {total - len(pipes) - len(valid_out)}")

main_expand(mat, set(locs))