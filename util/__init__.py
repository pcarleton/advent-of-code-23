

def strl(ns):
    return [int(s) for s in ns.strip().split()]

def mkpairs(l):
    return [(l[i], l[i+1]) for i in range(0, len(l), 2)]
