import collections


def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def getinfo(claim):
    """ Parses claim of form '#X @ n,m: pxq' to return n,m,p,q. """

    # Remove '#X @'
    stripped = claim.split('@')
    stripped = stripped[1].split(':')

    # Remove leading whitespace
    stripped = [info.strip() for info in stripped]
    margins = stripped[0].split(',')
    size = stripped[1].split('x')

    return int(margins[0]), int(margins[1]), int(size[0]), int(size[1])


def getoverlaps(claims):
    """ Takes list of claims and get the number of squares present in at least two claims' area. """
    info = [getinfo(claim) for claim in claims]

    overlaps = collections.Counter()

    # Enumerate all squares which are in the area of some claim
    for claim in info:
        area = [(claim[0]+n, claim[1]+m) for n in range(claim[2]) for m in range(claim[3])]
        overlaps.update(area)

    # Find squares in at least two claims
    squares = list(dict(overlaps).keys())  # Get list of all used squares
    overlaps.subtract(squares)  # Decrement overlaps
    overlaps += collections.Counter()  # Remove items with zero or less counts

    overlapsquares = list(dict(overlaps).keys())  # Get list of all squares used at least twice

    return overlapsquares


def countoverlaps(claims):
    return len(getoverlaps(claims))


# Test of getinfo, expected output 7,8,9,6
print(getinfo('#69 @ 7,8: 9x6'))

# Test of trackoverlaps, expected output 4
print(countoverlaps(['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']))

# Actual input
print(countoverlaps(parse('D3input.txt')))
