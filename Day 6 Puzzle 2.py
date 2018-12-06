
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


def adddists(point, locations):
    """ Find closest locations to point according to L1 distance. """

    totaldist = 0  # Keep track of distances to each point
    for location in locations:
        dist = taxi(point, location)
        totaldist += dist

    return totaldist


def findarea(threshold, locations):
    """ Finds the area whose total distances to each location is below threshold. """

    # Get appropriately sized search radius - suffices to compute the mins and maxes in each dimension, as if
    # a point x is closest to some point y in locations, say e.g. on the right edge of the resulting square,
    # then x+(n,0) will be closest to y for all positive n as well, so the region corresponding to y will be
    # infinite.
    xmaxdim = max([tup[0] for tup in locations])
    xmindim = min([tup[0] for tup in locations])
    ymaxdim = max([tup[1] for tup in locations])
    ymindim = min([tup[1] for tup in locations])

    sizethreshold = 0

    # 'Useful region' will be range(xmindim, xmaxdim+1) cross range(ymindim, ymaxdim+1) by above argument.
    region = [(x, y) for x in range(xmindim-sizethreshold, xmaxdim+1+sizethreshold)
              for y in range(ymindim-sizethreshold, ymaxdim+1+sizethreshold)]

    area = 0

    # Loop through each point in 'useful region' and calculate L1 distances to points in locations.
    for point in region:
        totaldist = adddists(point, locations)

        if totaldist < threshold:
            area += 1

    return area


# Test of taxi, expected output 5
print(taxi((0, 0), (2, 3)))

# Test of findarea, expected output 16
print(findarea(32, [(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]))

# Actual input
print(findarea(10000, parse('D6input.txt')))
