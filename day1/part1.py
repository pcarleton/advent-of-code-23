


def first_digit(s):
    for c in s:
        if c.isdigit():
            return c

def last_digit(s):
    for c in s[::-1]:
        if c.isdigit():
            return c

def process(data):
    # print(data)
    
    calibration = 0
    for line in data.split("\n"):
        calibration += int(first_digit(line) + last_digit(line))
    
    return calibration
        




def main():
    with open("./day1/test1") as fh:
        print(process(fh.read()))

    with open("./day1/input1.txt") as fh:
        print(process(fh.read()))



if __name__ == "__main__":
    main()
