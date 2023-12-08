


class Interval:

    def __init__(self, start, end):
        self.start = start
        self.end = end


    def __str__(self) -> str:
        return f'[{self.start}, {self.end})'
    

    def __eq__(self, other: object) -> bool:
        return self.start == other.start and self.end == other.end

    def intersect(self, other):
        # [0, 5],  [3, 10] ==> [3, 5]
        if self.end < other.start or self.start > other.end:
            return None

        return Interval(max(self.start, other.start), min(self.end, other.end))
    


assert Interval(0, 5).intersect(Interval(3, 10)) == Interval(3, 5)

print(Interval(0, 5).intersect(Interval(10, 21)))