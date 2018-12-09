def parse(filename):
    """ Reads file into list while stripping away whitespace characters, expecting tuples """
    with open(filename) as file:
        lines = [line.strip() for line in file]

    scrubbedlines = list()

    for line in lines:
        splitline = line.split(' ')
        scrubbedline = (splitline[1], splitline[7])
        scrubbedlines.append(scrubbedline)

    return scrubbedlines


def linearize(pairs):
    """ Given a list of pairs (as in a partial order), compute a linearization of that order.
    To break ties, go in alphabetical order.
    """

    initials = set([pair[0] for pair in pairs])
    terminals = set([pair[1] for pair in pairs])
    elements = initials.union(terminals)

    # Build a dictionary that records the set of elements below a given element (to be thought of as conditions), i.e.
    # the downsets of each element in the poset.

    downsets = dict()

    for pair in pairs:
        if pair[1] in downsets.keys():
            downsets[pair[1]].add(pair[0])
        else:
            downsets[pair[1]] = {pair[0]}

    for element in initials.difference(terminals):
        downsets[element] = set()

    linearization = list()  # The intended output
    used = set()  # Keep track of conditions fulfilled
    unused = elements  # Keep track of conditions unfulfilled
    usable = initials.difference(terminals)  # These elements have no conditions

    # While there are still usable elements, get the smallest (alphabetically) and append to our linearization.
    # Then update used, unused. To update usable, loop through unused elements to see if their conditions have
    # been met.
    while usable:
        nextelement = min(usable)
        linearization.append(nextelement)
        used.add(nextelement)
        unused.remove(nextelement)
        usable.remove(nextelement)

        for element in unused:
            if downsets[element].issubset(used):
                usable.add(element)

    return ''.join(linearization)


# Test of linearize, expected output 'CABDFE'
print(linearize([('C', 'A'), ('C', 'F'), ('A', 'B'), ('A', 'D'), ('B', 'E'), ('D', 'E'), ('F', 'E')]))

print(linearize(parse('D7testinput.txt')))

# Actual input
print(linearize(parse('D7input.txt')))
