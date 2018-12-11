def getdigit(x, index):
    xmod = x % 10**(index+1)
    if index > 0:
        xfract = x % 10**index
        xmod = xmod - xfract
        xmod = xmod/(10**index)
    return int(xmod)


def findpowerlevel(x, y, serial):
    rackid = x+10
    powerlevel = rackid * y
    powerlevel += serial
    powerlevel = powerlevel * rackid
    powerlevel = getdigit(powerlevel, 2)  # Get hundreds digit
    powerlevel -= 5

    return powerlevel


def populatepowerlevels(serial, size):
    """ Population size x size grid with power levels. """

    grid = dict()
    for x in range(1, size+1):
        for y in range(1, size+1):
            grid[(x, y)] = findpowerlevel(x, y, serial)

    return grid


def findsquare(serial, gridsize):
    """ Find squaresize x squaresize sub-square of grid (of dimension gridsize x gridsize)
    with highest total powerlevel. """

    grid = populatepowerlevels(serial, gridsize)

    gridsquares = dict()
    for x in range(1, gridsize+1):
        for y in range(1, gridsize+1):
            gridsquares[(x, y, 1)] = grid[(x, y)]

    for squaresize in range(2, gridsize):
        for x in range(1, gridsize-squaresize+1):
            for y in range(1, gridsize-squaresize+1):
                gridsquares[(x, y, squaresize)] = gridsquares[(x, y, squaresize-1)]
                for suby in range(y, y+squaresize):
                    gridsquares[(x, y, squaresize)] += grid[(x+squaresize-1, suby)]
                for subx in range(x, x+squaresize-1):
                    gridsquares[(x, y, squaresize)] += grid[(subx, y+squaresize-1)]

    return max(gridsquares, key=gridsquares.get)


# Test of getdigit
print(getdigit(12345, 2))  # Expected output 3
print(getdigit(5, 2))  # Expected output 0

# Test of findpowerlevel
print(findpowerlevel(3, 5, 8))  # Expected output 4
print(findpowerlevel(33, 45, 18))  # Expected output 4

# Test of findsquare
print(findsquare(18, 300))  # Expected output (90, 269, 16)

# Actual input
print(findsquare(4842, 300))
