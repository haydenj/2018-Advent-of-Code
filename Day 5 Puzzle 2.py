def parse(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines[0]


def reduce(seq):
    currentlength = len(seq)

    reductions = ['aA', 'Aa', 'bB', 'Bb', 'cC', 'Cc', 'dD', 'Dd', 'eE', 'Ee', 'fF', 'Ff', 'gG', 'Gg', 'hH', 'Hh',
                  'iI', 'Ii', 'jJ', 'Jj', 'kK', 'Kk', 'lL', 'Ll', 'mM', 'Mm', 'nN', 'Nn', 'oO', 'Oo', 'pP', 'Pp',
                  'qQ', 'Qq', 'rR', 'Rr', 'sS', 'Ss', 'tT', 'Tt', 'uU', 'Uu', 'vV', 'Vv', 'wW', 'Ww', 'xX', 'Xx',
                  'yY', 'Yy', 'zZ', 'Zz']

    while True:
        for reduction in reductions:
            seq = seq.replace(reduction, '')
        if len(seq) == currentlength:
            break
        else:
            currentlength = len(seq)

    return currentlength


def findbadunit(seq):
    alpha = list('abcdefghijklmnopqrstuvwxyz')

    unitcounts = dict()

    for unit in alpha:
        removedseq = seq.replace(unit, '')
        removedseq = removedseq.replace(unit.capitalize(), '')
        unitcounts[unit] = reduce(removedseq)

    minunit = min(unitcounts, key=unitcounts.get)
    minlength = unitcounts[minunit]

    return minunit, minlength


# Test of reduce, expected output 10
print(reduce('dabAcCaCBAcCcaDA'))

# Test of findbadunit, expected output
print(findbadunit('dabAcCaCBAcCcaDA'))

# Actual input
print(findbadunit(parse('D5input.txt')))
