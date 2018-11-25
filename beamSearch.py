import heapq
import math
import random

cost_dict = {'w' : math.inf, 'm' : 100, 'p' : 10, 's' : 30}

class Node():

    def __init__(self, parent = None, location = None):
        self.parent = parent
        self.localtion = location

        # cost function
        self.f = 0
        # Heuristic
        self.h = 0
        self.g = self.f + self.h

def goalTest(curr, goal):
    if curr == goal:
        return True
    return False


def surrounding_spaces(startNode, mat):
    # Check if the agent is near the border of the maze
    x = startNode.localtion[0]
    y = startNode.localtion[1]
    observable = []
    # North Neighbor
    if x-1 >= 0:
        observable.append((x-1, y))
    # East Neighbor
    if y+1 <= len(mat) - 1:
        observable.append((x, y+1))
    # South Neighbor
    if x+1 <= len(mat) - 1:
        observable.append((x+1,y))
    # West Neighbor
    if y-1 >= 0:
        observable.append((x, y-1))
    # North east neighbor
    if x-1 >= 0 and y+1 <= len(mat) - 1 and mat[x-1][y+1] != 'w':
        observable.append((x-1, y+1))
    # South East Neighbor
    if x+1 <= len(mat) - 1 and y+1 <= len(mat) - 1 and mat[x+1][y+1] != 'w':
        observable.append((x+1, y+1))
    # South West Neighbor
    if x+1 <= len(mat) - 1 and y-1 >= 0 and mat[x][y-1] != 'w':
        observable.append((x+1, y-1))
    # North West Neighbor
    if x-1 >= 0 and y-1 >= 0 and mat[x-1][y-1] != 'w':
        observable.append((x-1, y-1))

    return observable

def findWalls(ifWall, parent):

    if mat[parent.localtion[0]-1][parent.localtion[1]+1] == 'w':
        ifWall[(parent.localtion[0]-1, parent.localtion[1]+1)] = True
    else:
        ifWall[(parent.localtion[0] - 1, parent.localtion[1] + 1)] = False

    if mat[parent.localtion[0]-1][parent.localtion[1]-1] == 'w':
        ifWall[(parent.localtion[0]-1, parent.localtion[1]-1)] = True
    else:
        ifWall[(parent.localtion[0] - 1, parent.localtion[1] - 1)] = False

    if mat[parent.localtion[0]+1][parent.localtion[1]+1] == 'w':
        ifWall[(parent.localtion[0]+1, parent.localtion[1]+1)] = True
    else:
        ifWall[(parent.localtion[0] + 1, parent.localtion[1] + 1)] = False

    if mat[parent.localtion[0]+1][parent.localtion[1]-1] == 'w':
        ifWall[(parent.localtion[0]+1, parent.localtion[1]-1)] = True
    else:
        ifWall[(parent.localtion[0] + 1, parent.localtion[1] - 1)] = False


def findNextMove(observable, mat, parent):
    available_moves = {}
    ifWall = {}
    findWalls(ifWall, parent)
    for loc in observable:
        if mat[loc[0]][loc[1]] != 'w':
            score = 0
            if loc[0]==0 or loc[0]==len(mat):
                score = -math.inf
            if loc[1] == 0 or loc[1] == len(mat):
                score = -math.inf
            # North
            # northOfThis = (loc[0]-1, loc[1])
            # southOfThis = (loc[0]+1, loc[1])
            # eastOfThis = (loc[0], loc[1]+1)
            # westOfThis = (loc[0], loc[1]-1)

            available_moves[loc] = score

    print(available_moves)


def solve(start, goal, mat):
    startNode = Node(None, start)
    endNode = Node(None, goal)
    curr = startNode
    observable = surrounding_spaces(curr, mat)
    traversed = []
    print(observable)
    while (goal not in observable):
        observable = surrounding_spaces(curr, mat)
        chosenTile = findNextMove(observable, mat, curr)

if __name__ == '__main__':
    mat = [['w','w','w','w','w','w','w','p'],
           ['m','m','s','s','s','p','p','w'],
           ['s','s','p','s','p','s','m','w'],
           ['p','w','m','s','s','s','w','w'],
           ['w','w','m','w','w','m','p','p'],
           ['w','p','w','w','s','p','w','m'],
           ['m','s','s','w','w','p','p','p'],
           ['s','s','p','m','m','p','w','w']]
    path = solve((6,7), (6,2), mat)
