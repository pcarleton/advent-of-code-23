D = open("./day7/input.txt").readlines()

# print(D)
prob = [(x, int(y)) for x, y in [[g for g in l.strip().split(" ")] for l in D]]

card_order = 'AKQJT98765432'
clut = {c: i for i, c in enumerate(card_order[::-1])}

hand_order = [
    'five',
    'four',
    'full',
    'three',
    'dpair',
    'pair',
    'high'
]
hlut = {h: i for i, h in enumerate(hand_order[::-1])}

import collections

def lbl_card(hand):
    cnt = collections.Counter(hand)
    b = cnt.most_common()
    top_c = b[0][1]

    if top_c >= 5:
        return 'five'
    elif top_c == 4:
        return 'four'

    next_ct = b[1][1]
    if top_c == 3:
        if next_ct == 2:
            return 'full'
        return 'three'
    
    if top_c == 2:
        if next_ct == 2:
            return 'dpair'
        return 'pair'

    return 'high'


def hand_sort_key(hand):
    return (hlut[lbl_card(hand)],) + tuple(clut[c] for c in hand)

shands = sorted(prob, key=lambda h: hand_sort_key(h[0]))

# print(shands)

score = sum([i*h[1] for i, h in enumerate(shands, 1)])

print(f"part1: {score}")


card_order = 'AKQT98765432J'
clut = {c: i for i, c in enumerate(card_order[::-1])}

def new_lbl(hand):
    lbls = [lbl_card(hand)]
    if 'J' not in hand:
        return hlut[lbls[0]]
    
    cnt = collections.Counter(hand)
    j_count = cnt['J']
    del cnt['J']
    
    for ca, _ in cnt.most_common():
       h = "".join(cnt.elements()) + ca*j_count
       lbls.append(lbl_card(h))

    return max(hlut[l] for l in lbls)

def hand_sort_key2(hand):
    return (new_lbl(hand),) + tuple(clut[c] for c in hand)

shands = sorted(prob, key=lambda h: hand_sort_key2(h[0]))
score = sum([i*h[1] for i, h in enumerate(shands, 1)])

print(f"part2: {score}")