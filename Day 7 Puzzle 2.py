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


def linearize(teamsize, plus, pairs):
    """ Given a list of pairs of tasks (as in a partial order), compute a linearization of that order and the amount of
    time needed to complete those tasks in the determined order. Some number (teamsize) of workers work simultaneously
    on the steps, which each take 'plus+[place in the alphabet]' time to complete. When doling out new tasks, go by
    alphabetical order.
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

    # Keep track of the step a worker is working on as well as the amount of time left to complete it
    time = 0
    workerstime = list()
    workersstep = list()
    for worker in range(teamsize):
        workerstime.append(None)
        workersstep.append(None)

    # Create mapping relating the step to how long it takes
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = list(alphabet)
    steptime = dict()
    for index in range(len(alphabet)):
        steptime[alphabet[index]] = index+1

    inprocess = set()  # Keep track of what is currently being worked on by a worker

    # For each worker, determine if they have finished a task; if so, add it to the linearization and update everything.
    # Then update usable, looking at unused elements that are not in the process of being completed.
    # Finally, hand out tasks to workers who are currently idle.
    while unused:
        for worker in range(teamsize):
            if workerstime[worker] is not None:
                workerstime[worker] -= 1
            if workerstime[worker] == 0:
                linearization.append(workersstep[worker])
                used.add(workersstep[worker])
                inprocess.remove(workersstep[worker])
                unused.remove(workersstep[worker])
                workerstime[worker] = None
                workersstep[worker] = None

        for element in unused.difference(inprocess):
            if downsets[element].issubset(used):
                usable.add(element)

        for worker in range(teamsize):
            if workersstep[worker] is None and usable:
                nextelement = min(usable)
                workersstep[worker] = nextelement
                workerstime[worker] = plus+steptime[nextelement]
                inprocess.add(nextelement)
                usable.remove(nextelement)

        time += 1

    return time-1, ''.join(linearization)


# Test of linearize, expected output '15, CABDFE'
print(linearize(2, 0, [('C', 'A'), ('C', 'F'), ('A', 'B'), ('A', 'D'), ('B', 'E'), ('D', 'E'), ('F', 'E')]))

print(linearize(2, 0, parse('D7testinput.txt')))

# Actual input
print(linearize(5, 60, parse('D7input.txt')))
