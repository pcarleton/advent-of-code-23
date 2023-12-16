from util import *

import heapq


# input = "./day11/test.txt"
input = "./day11/input.txt"

D = open(input).readlines()

mat = [l.strip() for l in D]


gals1 = [(x, y) for x in range(len(mat[0])) for y in range(len(mat)) if mat[y][x] == '#']

# print(gals1)

def get_exps(gals):
    xs = set(x[0] for x in gals)
    ys = set(x[1] for x in gals)
    zero_rows = [i for i in range(len(mat)) if i not in ys]
    zero_cols = [col for col in range(len(mat[0])) if col not in xs]
    return zero_rows, zero_cols

from collections import defaultdict, deque


xpand_mult = 1000000
def expand_x(gals, x_cols, y_rows):
    galrs = defaultdict(list)
    for g in gals:
        galrs[g[1]].append(g)

    galrs = {k: deque(sorted(v)) for k, v in galrs.items()}

    c_idx = 0
    r_idx = 0
    r_delta = 0
    ngs = []
    for r in sorted(galrs.keys()):
        ps = galrs[r]
        while r_idx < len(y_rows) and r > y_rows[r_idx]:
            r_idx += 1
            r_delta += 1*xpand_mult - 1
        
        c_idx = 0
        c_delta = 0
        while len(ps) > 0:
            np = ps.popleft() #heapq.heappop(ps)
            while c_idx < len(x_cols) and np[0] > x_cols[c_idx]:
                c_idx += 1
                c_delta += 1*xpand_mult - 1
            
            ngs.append((np[0]+c_delta, np[1]+r_delta))

    return set(ngs)


def pgal(gal):
    max_x = int(max(x[0] for x in gal))
    max_y = int(max(x[1] for x in gal))

    print("\n".join([''.join(['#' if (x, y) in gal else '.' for x in range(max_x+1)]) for y in range(max_y+1)]))


# pgal(gals1)

r, c = get_exps(gals1)
# print(r, c)

ng = expand_x(gals1, c, r)
# print(ng)
# pgal(ng)

import itertools

def dist(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])

mdists = [dist(g1, g2) for g1, g2 in itertools.combinations(ng, 2)]

print("part1:", sum(mdists))



