

def strl(ns, s=''):
    return [int(s) for s in ns.strip().split(s)]


def splitdn(text):
    return text.split("\n\n")

def mkpairs(l):
    return [(l[i], l[i+1]) for i in range(0, len(l), 2)]

GREEN = "\033[0;32m"
RED = "\033[0;31m"
BLUE = "\033[0;34m"
YELLOW = "\033[0;33m"

END = "\033[0m"
GREEN_BG = "\033[0;42m"

def ansi_color(s, color):
    return f"{color}{s}{END}"

def colorize(x, y, c, csets):
    for color, coordset in csets:
        if (x,y) in coordset:
            return ansi_color(c, color)
    
    return c

def icolorize(p, c, csets):
    for color, coordset in csets:
        if p in coordset:
            return ansi_color(c, color)
    
    return c