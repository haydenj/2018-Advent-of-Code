import collections


def parse(filename):
    """ Reads file into list while stripping away whitespace characters, expecting tuples """
    with open(filename) as file:
        lines = [line.strip() for line in file]
        lines = [eval(line) for line in lines]

    return lines


def taxi(tup1, tup2):
    """ Compute taxi/L1/Manhattan distance between tuples tup1, tup2. """

    if len(tup1) != len(tup2):
        raise ValueError("Tuples must be of equal dimension.")

    length = 0
    for index in range(len(tup1)):
        length += abs(tup1[index]-tup2[index])

    return length


def getclosest(point, locations):
    """ Find closest locations to point according to L1 distance. """

    distances = dict()  # Keep track of distances to each point
    for location in locations:
        dist = taxi(point, location)
        distances[location] = dist

    closestdist = min(distances.values())
    closest = [location for location, dist in distances.items() if dist == closestdist]

    return closest


def findarea(locations):
    """ Finds the largest (finite) area of points closest to given locations (wrt L1 distance). """

    # Get appropriately sized search radius - suffices to compute the mins and maxes in each dimension, as if
    # a point x is closest to some point y in locations, say e.g. on the right edge of the resulting square,
    # then x+(n,0) will be closest to y for all positive n as well, so the region corresponding to y will be
    # infinite.
    xmaxdim = max([tup[0] for tup in locations])
    xmindim = min([tup[0] for tup in locations])
    ymaxdim = max([tup[1] for tup in locations])
    ymindim = min([tup[1] for tup in locations])

    # 'Useful region' will be range(xmindim, xmaxdim+1) cross range(ymindim, ymaxdim+1) by above argument.
    region = [(x, y) for x in range(xmindim, xmaxdim+1) for y in range(ymindim, ymaxdim+1)]

    areas = collections.Counter()  # Use Counter to keep track of number of points attributed to each location.

    # Loop through each point in 'useful region' and calculate L1 distances to points in locations.
    for point in region:
        closest = getclosest(point, locations)

        if len(closest) == 1:
            areas[closest[0]] += 1

    # To determine locations with infinite associated set of closest points, rerun for outer boundary and
    # any location whose count increases must be have infinite associated set.

    outer = [(x, y) for x in [xmindim-1, xmaxdim+1] for y in range(ymindim-1, ymaxdim+2)] + \
            [(x, y) for x in range(xmindim-1, xmaxdim+2) for y in [ymindim-1, ymaxdim+1]]

    for point in outer:
        closest = getclosest(point, locations)

        if len(closest) == 1:
            areas[closest[0]] = 0

    return max(dict(areas).values())


# Test of taxi, expected output 5
print(taxi((0, 0), (2, 3)))

# Test of getclosest, expected output (5, 5)
print(getclosest((5, 4), [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]))

# Test of findarea, expected output 17
print(findarea([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]))

# Actual input
print(findarea(parse('D6input.txt')))
