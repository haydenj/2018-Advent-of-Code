import collections


def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def countletter(wordlist):
    """ Accepts a list of strings and parses each to record number of instances of each letter. """

    twocount = 0
    threecount = 0

    for word in wordlist:
        wordcount = collections.Counter(word)  # Counter object records # of instances of each letter in word
        counts = dict(wordcount).values()  # Get list of number of instances

        if 2 in counts:
            twocount += 1
        if 3 in counts:
            threecount += 1

    return twocount, threecount


def checksum(tup):
    return tup[0]*tup[1]


# Test of countletter, expected output 2, 1
print(countletter(['aa', 'aaa', 'aabb', 'a']))

# Run on actual input
print(checksum(countletter(parse('D2input.txt'))))
