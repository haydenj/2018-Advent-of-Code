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


# Test of reduce, expected output 10
print(reduce('dabAcCaCBAcCcaDA'))

# Actual input
print(reduce(parse('D5input.txt')))
