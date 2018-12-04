import collections


def parse(filename):
    """ Reads file into list while stripping away whitespace characters. """
    with open(filename) as file:
        lines = [line.strip() for line in file]
    return lines


def getinfo(timestamp):
    """ Parse timestamp to get date, hour, minute info, along with extra
    information which either records a change in state (asleep or awake)."""
    datetime, message = timestamp.split(']')

    date, time = datetime.split()
    date = date.strip('[')
    hour, minute = time.split(':')

    message = message.split()
    extra = message[1]  # either 'asleep', 'up', or '#XXX'

    return date, int(hour), int(minute), extra


def getminute(timestamps):
    timestamps.sort()  # Sort timestamps to get appropriate guard number
    timestamps = [getinfo(timestamp) for timestamp in timestamps]  # Parse each timestamp

    minutecounts = dict()  # Keep track of each minute of the hour a guard sleeps
    timecounts = dict()  # Keep track of total time asleep per guard

    currentguard = None
    timeasleep = None

    for timestamp in timestamps:
        date, hour, minute, extra = timestamp

        if extra[0] == '#':
            currentguard = extra
        elif extra == 'asleep':
            timeasleep = minute
        elif extra == 'up':
            timeawake = minute
            timeelapsed = timeawake - timeasleep

            if currentguard not in timecounts.keys():
                timecounts[currentguard] = 0
            timecounts[currentguard] += timeelapsed

            for minute in range(timeasleep, timeawake):
                if currentguard not in minutecounts.keys():
                    minutecounts[currentguard] = collections.Counter()
                minutecounts[currentguard][minute] += 1

    guard = max(timecounts, key=timecounts.get)  # Get guard with most time asleep
    minute = minutecounts[guard].most_common(1)

    return guard, minute


# Test of getinfo, expected output '1518-11-01', 0, 30, 'asleep'
print(getinfo('[1518-11-01 00:30] falls asleep'))

# Test of getminute, expected output '#10', 24
print(getminute(['[1518-11-01 00:00] Guard #10 begins shift', '[1518-11-01 00:05] falls asleep',
                 '[1518-11-01 00:25] wakes up', '[1518-11-01 00:30] falls asleep', '[1518-11-01 00:55] wakes up',
                 '[1518-11-01 23:58] Guard #99 begins shift', '[1518-11-02 00:40] falls asleep',
                 '[1518-11-02 00:50] wakes up', '[1518-11-03 00:05] Guard #10 begins shift',
                 '[1518-11-03 00:24] falls asleep', '[1518-11-03 00:29] wakes up',
                 '[1518-11-04 00:02] Guard #99 begins shift', '[1518-11-04 00:36] falls asleep',
                 '[1518-11-04 00:46] wakes up', '[1518-11-05 00:03] Guard #99 begins shift',
                 '[1518-11-05 00:45] falls asleep', '[1518-11-05 00:55] wakes up']))

print(getminute(parse('D4input.txt')))
