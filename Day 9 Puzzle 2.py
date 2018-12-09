from collections import deque


def playgame(playercount, lastmove):
    """ Play marble game with given number of players up to given lastmove.
        - At moves which are divisible by 23, add the move number and the marble which is
            counterclockwise 7 spaces of the current position to current player's score.
        - At all other moves, insert the new marble (with score equal to current move)
            clockwise two spaces from current position.

        Returns the winning score after playing the game to lastmove.
    """
    # Use deque for rotation to place current position at right end so that inserting and popping is fast.

    # Initialize
    marbles = deque([0])
    scores = [0] * playercount

    for move in range(1, lastmove+1):
        if move % 23:
            marbles.rotate(-1)  # Rotate clockwise by 1
            marbles.append(move)  # Appends to right (clockwise) of current position
        else:
            marbles.rotate(7)  # Rotate counterclockwise by 7
            removed = marbles.pop()  # Get the removed marble's score
            scores[(move - 1) % playercount] += move + removed  # Increment current player's score
            marbles.rotate(-1)  # Rotate clockwise by 1

    return max(scores)


# Test of findmove
print(playgame(9, 32))  # expected output 32
print(playgame(10, 1618))  # expected output 8317
print(playgame(477, 70851))  # expected output 374690

# Actual input
print(playgame(477, 70851*100))
