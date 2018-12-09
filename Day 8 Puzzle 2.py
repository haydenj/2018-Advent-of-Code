def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]

    nums = lines[0].split(' ')
    return [int(num) for num in nums]


def gettree(root):
    """ Using the root of a tree, where a tree's node consists of four kinds of information:
        - a header, which consists of two numbers:
            - the number of children
            - the number of metadata entries
        - zero or more child nodes (as specified in the header)
        - one or more metadata entries (as specified in the header)
    The output is a list of each node and its metadata (numbered depth-first) and a dictionary which encodes the
    children relation.
    """
    # nodelist initially keeps track of the node number (numbered depth-first) and the number of children and
    # number of metadata entries
    nodelist = list()
    children = dict()

    revroot = root[::-1]  # reverse the root for easy popping
    currentnode = list()  # Stack to keep track of depth in tree

    # Initialization with root
    nodelist.append([0, revroot.pop(), revroot.pop()])
    currentnode.append(0)
    children[0] = list()

    # Go through the root's data
    while revroot:
        # Get the current parent node via the stack
        parent = currentnode[-1]

        # If every child of the parent has already been addressed, then the next info in revroot will be the
        # metadata, so collect metadata and append to nodelist's entry for the parent.
        if nodelist[parent][1] == 0:
            metadata = list()
            for datum in range(nodelist[parent][2]):
                metadata.append(revroot.pop())
            nodelist[parent].append(metadata)
            currentnode.pop()  # Done with parent
        # Otherwise, add the next child to the nodelist and stack.
        else:

            nodenum = len(nodelist)  # Name child
            # Include nodenum (name), number of children, and number of metadata entries
            nodelist.append([nodenum, revroot.pop(), revroot.pop()])
            nodelist[parent][1] -= 1  # Decrement number of remaining children of parent.

            children[nodenum] = list()  # Initialize child list for new child
            children[parent].append(nodenum)  # Update children entry for parent with new child

            currentnode.append(nodenum)  # Update stack

    # Delete the number of children and number of metadata from nodelist entries.
    for node in nodelist:
        node.pop(1)
        node.pop(1)

    return nodelist, children


def gettotal(root):
    """ Calculate total for each node in tree, defined as follows:
        - the total of a leaf is the sum of its metadata entries
        - the total of a non-leaf is the sum of the totals of the children as referenced by the node's
            metadata entries (1-indexed) when the reference refers to an actual child.
    """
    totals = dict()  # Track totals in dictionary

    nodelist, children = gettree(root)

    # Go through nodelist backwards to calculate totals
    revnodelist = nodelist[::-1]

    for node in revnodelist:
        nodenum = node[0]
        metadata = node[1]

        # If the node is a leaf, then the total is the sum of the metadata entries
        if not children[nodenum]:
            total = sum(metadata)
            totals[nodenum] = total

        # Otherwise, use the metadata entries as references to the totals of children (1-indexed)
        else:
            total = 0
            for entry in metadata:
                if entry <= len(children[nodenum]):
                    total += totals[children[nodenum][entry-1]]  # Adjust for 1-indexing of children
                else:
                    pass
            totals[nodenum] = total

    return totals


# Test of gettree, expected output [[0, [1, 1, 2]], [1, [10, 11, 12]], [2, [2]], [3, [99]]],
# {0:[1, 2], 1:[], 2:[3], 3:[]}
print(gettree([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]))

# Test of gettotal, expected output 66
print(gettotal([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])[0])

# Actual input
print(gettotal(parse('D8input.txt'))[0])
