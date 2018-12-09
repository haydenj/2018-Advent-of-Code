class CircularList(list):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item % len(self))
        except ZeroDivisionError:
            raise IndexError('list index out of range')

    def insert(self, place, item):
        if place % len(self) == 0:
            super().append(item)  # Always append to end when possible
        else:
            try:
                return super().insert(place % len(self), item)
            except ZeroDivisionError:
                return super().append(item)

    def pop(self, place=None):
        try:
            return super().pop(place % len(self))
        except ZeroDivisionError:
            raise IndexError('list index out of range')


def initialize(playernum):
    """ Start marble game with marble 0 placed. """
    scores = [0] * playernum
    return 1, CircularList([0]), 0, scores


def advancegame(move, marbles, current, scores):
    """ Advance game, given game state.
        - At moves divisible by 23, add that score plus the marble number 7 marbles
            counterclockwise from current position to current player's score.
        - Otherwise, add new marble two marbles clockwise from current position.
    """

    playernum = len(scores)
    if move % 23:
        newcurrent = (current+2) % len(marbles)
        # Insert marble at end if possible, otherwise in newcurrent position.
        if not newcurrent:
            marbles.insert(len(marbles), move)  # Insert marble at end.
            current = len(marbles) - 1  # Account for incremented length
        else:
            marbles.insert(newcurrent, move)  # Insert marble within. (Slow, see Puzzle 2 solution!)
            current = newcurrent
    else:
        player = move % playernum  # Get player position
        current = (current - 7) % len(marbles)
        removed = marbles.pop(current)  # (Slow, see Puzzle 2 solution!)
        lastscore = move+removed
        scores[player-1] += lastscore  # Update score

    return move + 1, marbles, current, scores


def playgame(playernum, moves):
    """ Play marble game with given number of players and moves. """
    gamestate = initialize(playernum)

    while gamestate[0] <= moves:
        gamestate = advancegame(*gamestate)

    print(gamestate)

    return None


def findmove(playernum, moves):
    gamestate = initialize(playernum)

    while gamestate[0] <= moves:
        gamestate = advancegame(*gamestate)

    # return gamestate
    return max(gamestate[3])


# Test of CircularList
cycle = CircularList([10, 11, 12, 13, 14])
print(cycle[7])  # Expected output 12
cycle.insert(0, 7)
print(cycle)  # Expected output [10, 11, 0, 12, 13, 14]
print(cycle.pop(12))  # Expected output 10
print(cycle)  # Expected output [11, 0, 12, 13, 14]

# Test of initialize, expected output 1, [0], 0, [0, 0, 0, 0, 0, 0, 0, 0, 0]
game = initialize(9)
print(game)

# Test of advancegame, expected output 2, [0, 1], 1, [0, 0, 0, 0, 0, 0, 0, 0, 0]
game = advancegame(*game)
print(game)

# Test of playgame, expected output (26,
# [0, 16, 8, 17, 4, 18, 19, 2, 24, 20, 25, 10, 21, 5, 22, 11, 1, 12, 6, 13, 3, 14, 7, 15],
# 10, [0, 0, 0, 0, 32, 0, 0, 0, 0])
playgame(9, 25)

# Test of findmove, expected output 32
print(findmove(9, 32))

# Actual input
print(findmove(477, 70851))
