import collections


def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def removeletter(words, place):
    """ Removes the place-position letter from word in words and adds to counter. """

    counter = collections.Counter()

    for word in words:
        modword = list(word)
        try:
            del modword[place]
            modword = ''.join(modword)
            counter[modword] += 1
        except IndexError:
            pass

    return counter


def finddupe(words):
    """ Find first instance of two strings in words differing by single letter in same place
    and return common substring. """

    found = False
    index = 0
    dupe = None

    # get largest length of string in words
    bound = max([len(word) for word in words])

    while not found and index < bound:
        counter = removeletter(words, index)
        counts = dict(counter).values()
        if 2 in counts:
            found = True
            dupe = counter.most_common(1)[0][0]
        index += 1

    return dupe

# Test of removeletter, expected value Counter({'bc': 2, 'de': 1})
print(removeletter(['abc', 'bbc', 'cde'], 2))

# Test of finddupe, expected value 'bc'
print(finddupe(['abc', 'bbc', 'cde']))

# Actual input
print(finddupe(parse('D2input.txt')))
