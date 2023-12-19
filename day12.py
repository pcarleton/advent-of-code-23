from util import *

import re

input = "./day12/test.txt"
input = "./day12/input.txt"

D = open(input).readlines()

def parse_line(l):
    ts, ns = l.split(" ")
    ns = tuple(strl(ns, ','))
    #ts = re.split('\.+', ts)

    return ts, ns

def calc_score(ts):
    ts = [''.join(g) for _, g in itertools.groupby(ts)]
    return tuple([len(t) for t in ts if '#' in t])

def qinds(ts):
    return [i for i, c in enumerate(ts) if c == '?']

import itertools


cache = {}

def prefix(ts):
    idx = 0 
    while idx < len(ts) and ts[idx] == '#':
        idx +=1 
    return ts[:idx]

import functools

# @functools.cache
def all_opts(ts, targ):
    # print(ts, targ)
    if len(targ) == 0:
        return [ts]
    
    if len(ts) == 0:
        return []

    if ts[0] == '.':
        return ['.'+t for t in all_opts(ts[1:], targ)]
    
    if ts[0] == '?':
        return ['.' + t for t in all_opts(ts[1:], targ)] + all_opts('#'+ts[1:], targ)
    
    pfx = ts[:targ[0]]
    valid_pfx = all(x != '.' for x in pfx) and len(pfx) == targ[0]
    good_pfx_end = (targ[0] >= len(ts)) or (ts[targ[0]] != '#')
    if valid_pfx and good_pfx_end:
        # consume the ? if we need to
        # print('good#\n')
        return ['#'*len(pfx) + '.' + x for x in  all_opts(ts[len(pfx)+1:], targ[1:])]
    
    # print('bad#\n')
    return []


@functools.cache
def all_opts_fast(ts, targ):
    # print(ts, targ)
    if not ts:
        return len(targ) == 0
    
    if len(targ) == 0:
        return '#' not in ts

    if ts[0] == '.':
        return all_opts_fast(ts[1:], targ)
    
    if ts[0] == '?':
        return all_opts_fast(ts[1:], targ) + all_opts_fast('#'+ts[1:], targ)
    
    pfx = ts[:targ[0]]
    valid_pfx = all(x != '.' for x in pfx) and len(pfx) == targ[0]
    good_pfx_end = (targ[0] >= len(ts)) or (ts[targ[0]] != '#')
    if valid_pfx and good_pfx_end:
        # consume the ? if we need to
        # print('good#\n')
        return all_opts_fast(ts[len(pfx)+1:], targ[1:])
    
    # print('bad#\n')
    return 0

pin = [parse_line(l) for l in D]

# print(pin)


# for t, targ in pin:
#     print(t, targ)
#     print(all_opts(t, targ))
#     print()

print("part1", sum([len(all_opts(t, targ)) for t, targ in pin]))

# print("part1", [(t, targ, all_opts(t, targ)) for t, targ in pin])


def unfold(ts, ns):
    return "?".join([ts]*5), ns*5

unfolded = [unfold(t, targ) for t, targ in pin]
print("part2", sum([all_opts_fast(t, targ) for t, targ in unfolded]))
