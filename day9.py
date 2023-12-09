from collections import deque
from util import *

input = "./day9/test.txt"
input = "./day9/input.txt"

D = open(input).readlines()

seqs = [strl(l) for l in D]


def getds(seq):
    return [y-x for x,y in zip(seq, seq[1:])]

def expand_seq(seq):
    cur = seq
    sqs = [cur]
    while not all([x==0 for x in cur]):
        cur = getds(cur)
        sqs.append(cur)

    return sqs

def extrapolate(sqs):
    rev = sqs[::-1]
    for i, s in enumerate(rev):
        parent = rev[i-1][-1] if i > 0 else 0
        s.append(s[-1] + parent)

    return sqs[0][-1]

# ex = expand_seq(seqs[0])
# nx = extrapolate(ex)
exp = [expand_seq(s) for s in seqs]
answer1 = sum([extrapolate(s) for s in exp])
print(f"part 1: {answer1}")


def extrapleft(sqs):
    rev = [deque(l) for l in sqs[::-1]]
    for i, s in enumerate(rev):
        parent = rev[i-1][0] if i > 0 else 0
        s.appendleft(s[0] - parent)

    return rev[-1][0]


seqs = [strl(l) for l in D]
answer2 = sum([extrapleft(expand_seq(s)) for s in seqs])
print(f"part 2: {answer2}")