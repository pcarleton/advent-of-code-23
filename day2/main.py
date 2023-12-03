


def parse_line(line):
    game_id, _, vals = line.partition(":")
    gid = int(game_id.split()[-1])

    games = [g.split(",") for g in vals.split(";")]

    glist = []
    for gvals in games:
        vals = {}
        for v in gvals:
            num, color = v.strip().split(" ")
            vals[color] = int(num)
        glist.append(vals)

    return glist

def get_max(gvals):
    gtup = [(k, v) for g in gvals for k, v in g.items()]

    gmax = {}
    for k, v in gtup:
        gmax[k] = max(gmax.get(k, v), v)

    return gmax

def check_game(gmax):
    return gmax['red'] <= 12 and gmax['green'] <= 13 and gmax['blue'] <= 14


def power_game(gmax):
    return gmax['red']*gmax['blue']*gmax['green']

def process_input(lines):
    id_sum = 0
    for gid, line in enumerate(lines):

        gvals = parse_line(line)
        gmax = get_max(gvals)
        good_game = check_game(gmax)

        # print(gvals, gmax, good_game)

        if good_game:
            id_sum += gid + 1
    
    return id_sum


def process_input2(lines):
    power_sum = 0
    for gid, line in enumerate(lines):

        gvals = parse_line(line)
        gmax = get_max(gvals)
        power = power_game(gmax)

        # print(gvals, gmax, good_game)

        power_sum += power
    
    return power_sum



with open("./day2/test1.txt") as fh:
    test1 = process_input(fh.readlines())

    assert test1 == 8
    print("test input passed")


with open("./day2/input1.txt") as fh:
    print(f"Part 1: {process_input(fh.readlines())}")


with open("./day2/input1.txt") as fh:
    print(f"Part 2: {process_input2(fh.readlines())}")