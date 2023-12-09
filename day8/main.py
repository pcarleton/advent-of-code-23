D = open("./day8/input.txt").readlines()

seq = [0 if c == 'L' else 1 for c in D[0].strip()]

rest = D[2:]
# AAA = (BBB, CCC)
coords = [(x, tuple(y[1:-1].split(", "))) for x, y in [
     [s.strip() for s in l.split("=")] 
  for l in rest
]]

cmap = dict(coords)
# print(cmap)

# cur = 'AAA'
# steps = 0
# while cur != 'ZZZ':
#     idx = seq[steps % len(seq)]
#     cur = cmap[cur][idx]
#     # print(cur)
#     steps += 1

# print(steps)


curs = [k for k in cmap if k[-1] == 'A']
print(curs)


print(len(curs))

z_indicies = [] #[[] for c in curs]
# what's a cycle look like?
# a node we've been to before at a place in the sequence we've seen it before
for i, cur in enumerate(curs):
    steps = 0
    # while steps < 20000:
    while cur[-1] != 'Z':
        idx = seq[steps % len(seq)]
        cur = cmap[cur][idx]
        # if cur[-1] == 'Z':
        #     z_indicies[i].append(steps)
        steps += 1
    z_indicies.append(steps)

fz = z_indicies #[x[0] for x in z_indicies]

import math
print(math.lcm(*fz))

# print("\n".join([" ".join(["{:2}".format(z) for z in zs]) for zs in z_indicies]))


# diffs = [[zs[i+1] - zs[i] for i in range(len(zs) - 1)] for zs in z_indicies]
# print("\n".join([" ".join(["{:2}".format(z) for z in zs]) for zs in diffs]))

# What if I search for the shortest path?
# w

# steps = 0
# while not all(c[-1] == 'Z' for c in curs):
#     new_curs = []
#     for cur in curs:
#         idx = seq[steps % len(seq)]
#         new_curs.append(cmap[cur][idx])
    
#     curs = new_curs
#     steps += 1

# print(steps)

