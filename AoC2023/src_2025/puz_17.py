#with open('../testdata/17_testdata.dat') as f:
with open('../data/17_data.dat') as f:
    ma = [list(x.strip()) for x in f]
# load as list of lists, grid
# ma[row][colm]

import heapq

# size of grid
rows = len(ma)
cols = len(ma[0])

# define start and end points
pos0 = (0, 0)  # Top left
end0 = (rows-1, cols-1)  # Bottom right


# Dijkstra's algorithm (based on standard implementation from Claude.ai)
# Important point is that each state (node) is defined by (r ,c, dir, Ndir)
# The grid is defined on the fly, based on the rules from the problem

def prob1():
    # Priority queue: (distance, row, col, direction, Ndir )
    pq = [(0, *pos0, (0, 0), 0)]

    # Track shortest distance to each position
    distances = {pos0: 0}

    # Visited set
    visited = set()

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while pq:
        dist, r, c, d, Ndir = heapq.heappop(pq)

        # Skip if already visited
        if (r, c, d, Ndir) in visited:
            continue

        visited.add((r, c, d, Ndir))

        # Found destination
        if (r, c) == end0:
            print(dist)
            return dist

        # Check all possible neighbors
        for dnew in directions:
            # check the conditions from the puzzle
            if dnew == (-1*d[0], -1*d[1]):  # we can't go back same direction
                continue
            if Ndir == 3 and dnew == d:  # if we already moved 3 times in that dir skip
                continue

            dr, dc = dnew
            nr, nc = r + dr, c + dc
            if dnew == d:  #
                newNdir = Ndir + 1
            else:
                newNdir = 1

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                if (nr, nc, dnew, newNdir) in visited:
                    continue

                # Cost is current distance + cost to enter new cell
                new_dist = dist + int(ma[nr][nc])

                # Update if shorter path found
                # remember that this needs to be the full state leading to a node
                if (nr, nc, dnew, newNdir) not in distances or new_dist < distances[(nr, nc, dnew, newNdir)]:
                    distances[(nr, nc, dnew, newNdir)] = new_dist
                    heapq.heappush(pq, (new_dist, nr, nc, dnew, newNdir))


prob1()


# Part 2
# Same type of solution, but more complex rules
def prob2():
    # Priority queue: (distance, row, col, direction, Ndir )
    pq = [(0, *pos0, (0, 0), 0)]

    # Track shortest distance to each position
    distances = {pos0: 0}

    # Visited set
    visited = set()

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while pq:
        dist, r, c, d, Ndir = heapq.heappop(pq)

        # Skip if already visited
        if (r, c, d, Ndir) in visited:
            continue

        visited.add((r, c, d, Ndir))

        # Found destination
        if (r, c) == end0:
            print(dist)
            break
            #return dist

        # Check all possible moves

        for dnew in directions:
            # check the conditions from the puzzle
            if dnew == (-1*d[0], -1*d[1]):  # we can't go back same direction
                continue
            if Ndir == 10 and dnew == d:  # if we already moved 10 times in that dir skip
                continue
            if Ndir < 4 and dnew != d and d != (0, 0):  # we still need to go same dir            
                continue

            dr, dc = dnew
            nr, nc = r + dr, c + dc

            # Check boundary 
            if 0 > nr or nr >= rows or 0 > nc or nc >= cols:
                continue

            # If new direction check that we have enough space to move 4 
            if d != dnew and (0 > r + dr*4 or r + dr*4 >= rows or 0 > c + dc*4 or c + dc*4 >= cols):
                continue

            if dnew == d:  #
                newNdir = Ndir + 1
            else:
                newNdir = 1

            if (nr, nc, dnew, newNdir) in visited:
                continue

            # Cost is current distance + cost to enter new cell
            new_dist = dist + int(ma[nr][nc])

            # Update if shorter path found
            # remember that this needs to be the full state leading to a node
            if (nr, nc, dnew, newNdir) not in distances or new_dist < distances[(nr, nc, dnew, newNdir)]:
                distances[(nr, nc, dnew, newNdir)] = new_dist
                heapq.heappush(pq, (new_dist, nr, nc, dnew, newNdir))


prob2()
