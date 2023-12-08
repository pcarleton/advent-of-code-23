


def parse_input_line(line):
    _card_num, _, nums = line.partition(":")
    winning, _, have = nums.strip().partition("|")
    win_nums = [int(x) for x in winning.strip().split(" ") if x]
    have_nums = [int(x) for x in have.strip().split(" ") if x]

    return win_nums, have_nums


def calc_score(win, have):
    hset = set(have)
    wset = set(win)
    winhave = len(hset & wset)
    if winhave == 0:
        return 0
    return 2**(winhave - 1)

def part1(lines, verbose=False):
    total = 0
    for line in lines:
        w, h = parse_input_line(line)
        score = calc_score(w, h)
        if verbose:
            print((w,h,score))
        total += score
    return total

def part2(lines, verbose=False):
    total = 0
    card_counts = [1]*len(lines)
    card_sources = [((i,1),)for i in range(len(lines))]
    for i, line in enumerate(lines):
        w, h = parse_input_line(line)
        winners = len(set(w) & set(h))
        cur_count = card_counts[i]

        for j in range(winners):
            card_counts[i+j+1] += cur_count
            card_sources[i+j+1] = card_sources[i+j+1] + ((i, cur_count),)


    # print(card_counts)
    # print(card_sources)
    return sum(card_counts)

with open("./day4/test.txt") as fh:
    print(f"Test: {part1(fh.readlines())}")

with open("./day4/test.txt") as fh:
    print(f"Test pt2: {part2(fh.readlines())}")

with open("./day4/input.txt") as fh:
    print(f"Input pt1: {part1(fh.readlines())}")

with open("./day4/input.txt") as fh:
    print(f"Input pt2: {part2(fh.readlines())}")