def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def aggregatechanges(changes):
    """ Adds integer elements of a list. """
    runningtotal = 0
    for change in changes:
        runningtotal += int(change)  # int('-n')=-n and int('+n')=n
    return runningtotal


# Test of aggregatechanges, expected output -1
print(aggregatechanges(['-1', '+1', '-1']))

# Run on actual input
print(aggregatechanges(parse('D1P1input.txt')))
