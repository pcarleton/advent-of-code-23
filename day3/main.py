import collections
symbols = "!@#$%^&*()_+=-,/"

GREEN = "\033[0;32m"
RED = "\033[0;31m"

END = "\033[0m"
GREEN_BG = "\033[0;42m"

def ansi_color(s, color):
    return f"{color}{s}{END}"

def colorize(x, y, c, pts, good, bad):
    if (x,y) in good:
        return ansi_color(c, GREEN)
    
    if (x,y) in bad:
        return ansi_color(c, RED)
    
    return c

def annotate_mtx(mtx, pts, good, bad):
    annotated = "".join([
        "".join( colorize(x, y, c, pts, good, bad) for y, c in enumerate(row)        )
        for x, row in enumerate(mtx)
    ])

    return annotated


def find_adjacent(mtx):
    pts = []

    for x, row in enumerate(mtx):
        for y, c in enumerate(row):
            if c in symbols:
                pts.extend([
                    (x-1, y-1), (x -1, y+1), (x+1, y+1), (x+1, y-1),
                    (x-1, y), (x+1, y), (x, y-1), (x, y+1)])
                
    return pts

def find_gears(mtx):
    pts = []

    for x, row in enumerate(mtx):
        for y, c in enumerate(row):
            if c == '*':
                pts.append(
                    ((x,y),
                     ((x-1, y-1), (x -1, y+1), (x+1, y+1), (x+1, y-1), (x-1, y), (x+1, y), (x, y-1), (x, y+1)))
                )
                
    return pts


def find_row_numbers(row, x):
    i = 0

    digit = []
    pts = []
    dig_list = []
    while i < len(row):
        if not row[i].isdigit():
            if len(digit) > 0:
                dig = int("".join(digit))
                dig_list.append((dig, pts))
                digit, pts = [], []
        else:
            digit.append(row[i])
            pts.append((x, i))
        i += 1
    
    return dig_list


def find_numbers(mtx):
    m = []
    for x, row in enumerate(mtx):
        m.extend(find_row_numbers(row, x))

    return m


def process_pt2(lines):
    mtx = lines
    gears = find_gears(mtx)
    pnums = find_numbers(mtx)

    gmap = collections.defaultdict(list)

    good_pts = []
    for d, pts in pnums:
        for g, gpts in gears:
            if any(p in gpts for p in pts):
                gmap[g].append((d, pts))

    gear_ratio = 0
    for g, ds in gmap.items():
        if len(ds) == 2:
            for d, pts in ds:
                good_pts.extend(pts)
            gear_ratio += ds[0][0]*ds[1][0]

    print(annotate_mtx(mtx, [], good_pts, []))

    return gear_ratio



def process(lines):
    mtx = lines
    adj = find_adjacent(mtx)
    pnums = find_numbers(mtx)



    good_parts = []
    good_pts = []
    bad_pts = []
    for d, pts in pnums:
        if any(p in adj for p in pts):
            good_parts.append(d)
            good_pts.extend(pts)
        else:
            bad_pts.extend(pts)
            # print(f'bad: {d}')

    print(annotate_mtx(mtx, adj, good_pts, bad_pts))
    return sum(good_parts)

with open('./day3/test.txt') as fh:
    mtx = fh.readlines()
    print(f'Test input: {process(mtx)}')


# with open('./day3/input.txt') as fh:
#     # mtx = fh.readlines()
#     print("".join(set([c for l in fh.readlines() for c in l if not c.isdigit()])))



# with open('./day3/input.txt') as fh:
#     mtx = fh.readlines()
#     # print(find_row_numbers(mtx[0], 0))
#     print(f'Part 1: {process(mtx)}')


with open('./day3/test.txt') as fh:
    mtx = fh.readlines()
    print(f'Test input pt2: {process_pt2(mtx)}')

with open('./day3/input.txt') as fh:
    mtx = fh.readlines()
    # print(find_row_numbers(mtx[0], 0))
    print(f'Part 2: {process_pt2(mtx)}')