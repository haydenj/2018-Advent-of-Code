import numpy as np
import matplotlib.pyplot as plt


def parse(filename):
    """ Reads file into list while stripping away whitespace characters, expecting lines of the form
            'position=< X, Y> velocity=< U, V>'
        Returns numpy arrays of the positions and velocities (rows correspond to each coordinate)."""
    with open(filename) as file:
        lines = [line.strip() for line in file]

    positions = list()
    velocities = list()
    for line in lines:
        splitline = line.split('> ')
        position = splitline[0].split('<')[1].split(', ')
        velocity = splitline[1].split('<')[1].split(', ')
        posx = int(position[0])
        posy = int(position[1])
        velx = int(velocity[0])
        vely = int(velocity[1].strip('>'))

        positions.append([posx, posy])
        velocities.append([velx, vely])

    return np.array(positions).transpose(), np.array(velocities).transpose()


def xdiff(positions):
    """ Calculate the range of x-values of positions. """
    maxx = max(positions[0])
    minx = min(positions[0])

    return maxx-minx


def findmessage(positions, velocities):
    """ Find the hidden message as the positions are incremented by the velocities and
    return the time at which that message occured.
    """

    newpositions = positions
    nextsep = xdiff(newpositions)

    foundmin = False
    time = -1  # Start at -1 to account for discovering the correct time step by going one too far

    # Find the hidden message by minimizing the range of x-values.
    while not foundmin:
        lastsep = nextsep
        newpositions = newpositions + velocities
        nextsep = xdiff(newpositions)
        time += 1

        # If nextsep gets bigger, the previous time step is likely the message.
        if nextsep > lastsep:
            foundmin = True

    # Go back one time step to the minimizing one
    newpositions = newpositions - velocities
    plot(newpositions)

    return time


def plot(positions):
    """ Plot positions, where each row corresponds to the coordinate dimension. """
    xpos = positions[0]
    ypos = positions[1]
    plt.plot(xpos, ypos, 'ro')
    plt.show()
    return None


# Test of parse
# print(parse('D10testinput.txt'))

# Test of plot
# plot(parse('D10testinput.txt')[0])

# Test of findmessage, expected output 'HI' and 3
print(findmessage(*parse('D10testinput.txt')))

# Actual Input
print(findmessage(*parse('D10input.txt')))
