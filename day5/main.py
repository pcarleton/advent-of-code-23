import functools

def parse_ints(s):
    return [int(x) for x in s.strip().split(" ") if x]



@functools.cache
def do_mapping(x, intervals):
    for d, s, r in intervals:
        if s <= x < s+r:
            return x + (d-s)
        
    return x






def parse(fulltext):
    pieces = fulltext.split("\n\n")

    seeds = parse_ints(pieces[0].split(":")[1])

    maps = []
    for piece in pieces[1:]:
        lines = piece.split("\n")
        map_name = lines[0].split(" ")[0]

        intervals = tuple(tuple(parse_ints(s)) for s in lines[1:])

        maps.append((map_name, intervals))
    return maps, seeds

import collections

Rg = collections.namedtuple('Rg', ['dest', 'src', 'rng', 'src_end', 'delta', 'dest_end'])

def parse2(fulltext):
    pieces = fulltext.split("\n\n")

    seedranges = parse_ints(pieces[0].split(":")[1])
    seed_tupes = [seedranges[i:i+2] for i in range(0, len(seedranges), 2)]
    seeds = [(x, x+y) for x, y in seed_tupes]

    maps = []
    for piece in pieces[1:]:
        lines = piece.split("\n")
        map_name = lines[0].split(" ")[0]

        intervals = sorted(tuple(tuple(parse_ints(s)) for s in lines[1:]), key=lambda t: t[1])

        full_interval = [Rg(d, s, r, s+r, d-s, d+r) for d,s,r in intervals]

        maps.append((map_name, full_interval))
    return maps, seeds


def part1(fulltext):
    maps, seeds = parse(fulltext)

    locs = []
    for seed in seeds:
        s = seed
        # print("")
        for map_name, intervals in maps:
            # print(f'{map_name}, start: {s}')
            s = do_mapping(s, intervals)
        locs.append(s)

    return min(locs)


def print_rg(rg: Rg):
    print(f"[{rg.src}, {rg.src_end}) -> [{rg.dest}, {rg.dest_end}), △{rg.delta}")


def find_all_overlap(rg: Rg, rgs: [Rg]):
    overlaps = [inv for inv in rgs if inv.dest <= rg.src < inv.dest_end]

    # should only be 1
    assert len(overlaps) < 2
    if overlaps:
        return overlaps[0]
    
    # make an identity range
    # but wait, no need to know when it ends
    return Rg(rg.src, rg.src, rg.rng)
    

def do_mapping2(x, intervals):
    # print(intervals)
    for tup in intervals:
        if tup.src <= x < tup.src_end:
            return tup, None
        
        # we've overshot
        if x < tup.src:
            return None, tup

    return None, None

def part2(fulltext):
    maps, seed_ranges = parse2(fulltext)

    all_ranges = [seed_ranges]
    for i, mm in enumerate(maps):
        map_name, intervals = mm
        new_seed_ranges = []
        for rstart, rend in all_ranges[i]:
            p = rstart
            while p < rend:
                match, right = do_mapping2(p, intervals)
                
                if match:
                    new_p= min(rend, match.src_end)
                    new_range = (p+match.delta, new_p+match.delta)
                    new_seed_ranges.append(new_range)
                    p = new_p
                    continue

                if match is None and right is not None:
                    new_p = min(right.src, rend)
                    new_range = (p, new_p)
                    new_seed_ranges.append(new_range)
                    p = new_p
                    continue

                # no match
                new_seed_ranges.append((p, rend))
                break

        all_ranges.append(new_seed_ranges)
    
    return min([s for s, e in all_ranges[-1]])


def part2_abandon(fulltext):
    maps, seed_ranges = parse2(fulltext)



    locs = []
    i = 0

    ints = maps[-1][1]
    mer = ints[0]

    if mer.dest != 0:
        mer = Rg(0, 0, mer.dest, mer.dest, 0, mer.dest)

    print_rg(mer)
    # map it back
    # sec_to_last_range = (mer.src, mer.src_end)

    pre_ints = maps[-2][1]

    overlap = list(filter(lambda inv: inv.dest <= mer.src < inv.dest_end, pre_ints))[0]

    print(overlap)

    return 


    #overlap


    #  A depth first search:
    #  Start at the lowest interval in the last map (one starting with 0)
    #  find what intervals in the layer above that is mapped
    #  Pick the left most one, and keep mapping it up through the beginning
    #  becoming a narrower range
    
    # What do I need?
    #   given an interval, give me the intersecting intervals
    # So we have [56, 60), which is the lowest, and comes from range [93,97)
    # So now I want to go from [93,97) and see what sources map to that.
    # Oh actually! there's another interval, [0,56) which diretly maps
    # so that one shifts a little bit, it's [0,1) and [1,69)



# with open("./day5/test.txt") as fh:
#     print(part1(fh.read()))

# with open("./day5/input.txt") as fh:
#     print(part1(fh.read()))

with open("./day5/test.txt") as fh:
    print(part2(fh.read()))


with open("./day5/input.txt") as fh:
    print(part2(fh.read()))