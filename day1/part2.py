
import re

digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
dig_lookup = {d: i for i, d in enumerate(digits)}

flipped = [s[::-1] for s in digits]
flipped_lookup = {d: i for i, d in enumerate(flipped)}

DIG_REGEX = re.compile("|".join(digits) + "|[0-9]")
FLIPPED_REGEX = re.compile("|".join(flipped) + "|[0-9]")

def make_digit(s: str) -> int:
    if s.isdigit():
        return int(s)
    
    if s in dig_lookup:
        return dig_lookup[s]
    
    return flipped_lookup[s]

def process(data):
    # print(data)
    
    calibration = 0
    for line in data.split("\n"):
        # left = DIG_REGEX.search(line).group()
        # right = FLIPPED_REGEX.search(line[::-1]).group()
        # num = make_digit(left)*10 + make_digit(right)
        # print(line, left, right, num)

        # could do a search and reverse search, but this seems fine
        digits = DIG_REGEX.findall(line)
        num = make_digit(digits[0])*10 + make_digit(digits[-1])

        calibration += num
    
    return calibration
        




def main():
    with open("./day1/test2.txt") as fh:
        print(process(fh.read()))

    with open("./day1/input1.txt") as fh:
        print(process(fh.read()))


    # Attempt 1: 55929, failed to consider "eightwo" as "two" instead of "eight" for the last digit
    # Attempt 2: 55902


if __name__ == "__main__":
    main()
