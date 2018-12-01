# Forging-Path-AI
#Rishabh Sachdeva, Ajay Pal, Rohan Gujarathi, Kushal Mehta

import math
cost_dict = {'w': math.inf, 'm': 100, 'p': 10, 's': 30}
mat = None
path = ""

class Node():
#Captures parent and current location of node

    def __init__(self, parent=None, location=None):
        self.parent = parent
        self.location = location


def get_tile(observable, direction):
    return mat[observable[direction][0]][observable[direction][1]]


def surrounding_spaces(curr, maxlen):
    # Check if the agent is near the border of the maze
    x = curr.location[0]
    y = curr.location[1]
    observable = {}
    # North Neighbor
    if x-1 >= 0:
        observable['n'] = (x-1, y)
    # East Neighbor
    if y+1 <= maxlen - 1:
        observable['e'] = (x, y+1)
    # South Neighbor
    if x+1 <= maxlen - 1:
        observable['s'] = (x+1,y)
    # West Neighbor
    if y-1 >= 0:
        observable['w'] = (x, y-1)
    # North east neighbor
    if x-1 >= 0 and y+1 <= maxlen - 1 and not (get_tile(observable, 'n') == get_tile(observable, 'e') == 'w'):
        observable['ne'] = (x-1, y+1)
    # South East Neighbor
    if x+1 <= maxlen - 1 and y+1 <= maxlen - 1 and not (get_tile(observable, 's') == get_tile(observable, 'e') == 'w'):
        observable['se'] = (x+1, y+1)
    # South West Neighbor
    if x+1 <= maxlen - 1 and y-1 >= 0 and not (get_tile(observable, 's') == get_tile(observable, 'w') == 'w'):
        observable['sw'] = (x+1, y-1)
    # North West Neighbor
    if x-1 >= 0 and y-1 >= 0 and not (get_tile(observable, 'n') == get_tile(observable, 'w') == 'w'):
        observable['nw'] = (x-1, y-1)

    return observable


def find_movable(observable):
    # returns possible moves for agent.
    movable = {}
    for i in observable.keys():
        if i in ['n','w','s','e'] and mat[observable[i][0]][observable[i][1]] != 'w':
            x = observable[i][0]
            y = observable[i][1]
            movable[i] = observable[i]
    return movable

def deadend(current, explored):
    observableTiles = surrounding_spaces(current, len(mat))
    count = 0
    if 'e' not in observableTiles or get_tile(observableTiles, 'e') == 'w' or explored[observableTiles['e']]==math.inf:
        count+=1
    if 'w' not in observableTiles or get_tile(observableTiles, 'w') == 'w' or explored[observableTiles['w']]==math.inf:
        count += 1
    if 'n' not in observableTiles or get_tile(observableTiles, 'n') == 'w' or explored[observableTiles['n']]==math.inf:
        count += 1
    if 's' not in observableTiles or get_tile(observableTiles, 's') == 'w' or explored[observableTiles['s']]==math.inf:
        count += 1

    if count == 3:
        return True

    return False

# Building heuristic based on number_times_visited for a tile and locations(sand,mountainn and path)
def find_next_move(curr, observable, explored):
    # returns best next move
    global path
    movable_dict = find_movable(observable)
    #movable_dict : map <direction,location tuple>
    #explored : map<location, no. of times visited>
    scores={} # location tuple vs cost
    for k,v in movable_dict.items():
        #print(cost_dict[mat[v[0]][v[1]]],"path cost")
        #print(explored[v],"times visited")
        scores[k]=250*explored[v] + cost_dict[mat[v[0]][v[1]]]
    #list_of_movable = sorted(movable_dict.keys(), key=lambda x: explored[movable_dict[x]])#priority to unexplored or less visited
    #path += list_of_movable[0]
    dir = min(scores.items(), key=lambda x: x[1])[0]
    #print(scores,"score")
    #print(dir,"dir")
    path += dir
    return Node(curr, observable[dir])#observable[list_of_movable[0]])


def populate_explored(explored, observable):
    for v in observable.values():
        if v not in explored:
            explored[v] = 0


def update_explored(curr, explored):

    if deadend(curr,explored):
        explored[curr.location] = math.inf
    #print("inside wpdateExplored for" + str(curr.location))

    #updates explored location states. i.e. increments location pointer according to number of visits.
    explored[curr.location] += 1


def solve(start, goal, matrix):
    global mat
    mat = matrix
    start_node = Node(None, start)
    curr = start_node
    observable = surrounding_spaces(curr, len(mat))
    explored = dict()  # keeping track of what is explored
    explored[start_node.location] = 0
    steps = 0
    #while goal not in observable.values():
    populate_explored(explored, observable)
    update_explored(curr, explored)
    curr = find_next_move(curr, observable, explored)
    steps += 1
    observable = surrounding_spaces(curr, len(mat))
    #print(show_exploredmap(len(mat), explored))

    reachGoalInObservable(goal, observable)
    return path.upper()

def reachGoalInObservable(goal, observable):
    movable_dict = find_movable(observable)
    direction= ""
    global path
    #print(observable)
    for k,v in observable.items():
            if v == goal:
                direction = k
                break

    if goal in movable_dict.values():
        #in N,S,E,W, i.e. non diagnal
        path+=direction

    else:
        #see diagnals only
        f = direction[0]
        s = direction[1]
        fTile = get_tile(observable,f)
        sTile = get_tile(observable,s)
        fCost = cost_dict[fTile]
        sCost = cost_dict[sTile]
        if fCost>sCost:
            path += s+f
        else:
            path += f+s
'''
def show_exploredmap(length, explored):
    matrix =[[0 for _ in range(length)] for _ in range(length)]
    for k in explored.keys():
        matrix[k[0]][k[1]] = explored[k]
    for i in range(0,length):
        print(matrix[i])
'''


if __name__ == '__main__':
    mat = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'p'],
           ['m', 'm', 's', 's', 's', 'p', 'p', 'w'],
           ['s', 'w', 'p', 'w', 'p', 's', 'm', 'w'],
           ['p', 'w', 'm', 'w', 's', 's', 'w', 'w'],
           ['w', 'w', 'm', 'w', 'w', 'm', 'p', 'p'],
           ['w', 'p', 'w', 'w', 's', 'p', 'w', 'm'],
           ['m', 's', 's', 'w', 'w', 'p', 'p', 'p'],
           ['s', 's', 'p', 'm', 'm', 'p', 'w', 'w']]



    path = solve((0, 0), (7,0), mat)
    #path = solve((6, 7), (6,2), mat)
