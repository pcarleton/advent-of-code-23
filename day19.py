from util import *

input = "./day19/input.txt"
# input = "./day19/input.txt"

D = open(input).read()

from collections import namedtuple

Crit = namedtuple('Crit', ['r', 'd'])
Op = namedtuple('Op', ['f', 'op', 'v'])

# px{a<2006:qkq,m>2090:A,rfg}
def parse_rule(r):
    name, rest = r.split("{")
    rules = rest.strip("}").split(",")

    end = []
    for c in rules:
        ps = c.split(":")
        if len(ps) == 1:
            end.append(Crit(None, ps[0]))
        else:
            crit, dest = ps
            for sep in [">","<"]:
                if sep in crit:
                    f, o, v  = crit.partition(sep)
                    ops = (f, o, int(v))
                    end.append(Crit(Op(*ops), dest))

    return name, end

c1, c2 = splitdn(D)

def parse_piece(p):
    return {k: int(v) for k, v in [t.split("=") for t in p.strip("{}").split(",")]}

rules = {r[0]: r[1] for r in [parse_rule(l) for l in c1.split()]}
pieces = [parse_piece(p) for p in c2.split()]


def get_next(p, r):
    for c in r[:-1]:
        o = c.r
        v = p[o.f]
        if o.op == '<' and v < o.v:
            return c.d
        if o.op == '>' and v > o.v:
            return c.d

    return r[-1].d    

def process_piece(p):
    cur = 'in'
    while True:
        if cur == 'A':
            return True 
        if cur == 'R':
            return False
        cur = get_next(p, rules[cur])

accepted = list(filter(process_piece, pieces))
answer = sum([sum(p.values()) for p in accepted])

print(accepted, len(accepted))
print(f"part1: {answer}")
