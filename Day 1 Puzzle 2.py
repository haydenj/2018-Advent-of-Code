def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def aggregatechangesdupe(changes):
    """ Adds integer elements of a list while searching for first duplicate running total. """
    runningtotal = 0
    runningtotals = set()  # Create set for fast look-ups
    runningtotals.add(runningtotal)  # Initialize set

    duplicate = False

    # Loop through changes to get running totals and look-up whether duplicate has been found.
    while not duplicate:  # If no duplicate found, loop through again.
        for change in changes:
            runningtotal += int(change)  # int('-n')=-n and int('+n')=n
            if runningtotal in runningtotals:
                duplicate = runningtotal
                break
            else:
                runningtotals.add(runningtotal)

    return duplicate


# Test of aggregatechangesdupe, expected output -1
print(aggregatechangesdupe(['-1', '+2', '-2']))

# Run on actual input
print(aggregatechangesdupe(parse('D1P1input.txt')))
