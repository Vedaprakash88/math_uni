import queue


def maze1():
    grid2d = [[1, 1, 1, 1, 1, 'S', 1], [1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 0, 0, 1],
              [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 1, 0, 1],
              [1, 1, 1, 1, 1, 'F', 1]]

    return grid2d


def maze2():
    grid2d = [[1, 1, 1, 1, 1, 'S', 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 1, 1, 0, 1, 1, 0, 1], [1, 0, 1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1],
              [1, 0, 1, 0, 1, 0, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 1, 1, 1, 1, 1, 1, 'F', 1]]

    return grid2d

def valid(grid2d, moves):
    for x, pos in enumerate(grid2d[0]):
        if pos == 'S':
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

        if not (0 <= i < len(grid2d[0]) and 0 <= j < len(grid2d)):
            return False
        elif (grid2d[j][i] == 1):
            return False

    return True


def findEnd(grid2d, moves):
    for x, pos in enumerate(grid2d[0]):
        if pos == 'S':
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if grid2d[j][i] == 'F':
        print("Found: " + moves)
        printGrid2d(grid2d, moves)
        return True

    return False


def printGrid2d(grid2d, path=""):
    for x, pos in enumerate(grid2d[0]):
        if pos == 'S':
            start = x

    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))

    for j, row in enumerate(grid2d):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("⁛     ", end="")
            else:
                print(col, "    ", end="")
        print()

# MAIN ALGORITHM

nums = queue.Queue()
nums.put("")
add = ""
grid2d = maze2()
fnd = False
Fcnt = 0

for x in range(len(grid2d)):
    if 'F' in grid2d[x]:
        for y in range(len(grid2d[x])):
            if grid2d[x][y] == 'F':
                Fcnt += 1
        fnd = True

if fnd and Fcnt == 1:
    while not findEnd(grid2d, add):
        add = nums.get()
        # print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(grid2d, put):
                nums.put(put)
elif fnd == False:
    print("'F' not found in the given grid")
elif Fcnt > 1:
    print("More than 1 'F' in the grid")
