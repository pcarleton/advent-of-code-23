import functools

D = open("./day6/input.txt").readlines()

prob = list(zip(*[[int(s) for s in l.split(":")[1].strip().split(" ") if s] for l in D]))

# holding it down increases speed, but decreases time left
# so I think we want to find the intersection points with the current best time
def brute(dur, best):
    dists = [ (t*(dur-t)) for t in range(dur)]
    # print(dists)
    return len([d for d in dists if d > best])

print(functools.reduce(lambda acc, s: s*acc, [brute(t,b) for t,b in prob]))


prob2 = [int("".join([s for s in l.split(":")[1].strip().split(" ") if s])) for l in D]


print(brute(*prob2))
