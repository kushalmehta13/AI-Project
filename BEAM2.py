import math
cost_dict = {'w': math.inf, 'm': 100, 'p': 10, 's': 30}
mat = None
path = ""

class Node():

    def __init__(self, parent=None, location=None):
        self.parent = parent
        self.location = location
        #
        # # cost function
        # self.f = 0
        # # Heuristic
        # self.h = 0
        # self.g = self.f + self.h

#
# def goalTest(curr, goal):
#     if curr == goal:
#         return True
#     return False


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
    movable = {}
    for i in observable.keys():
        if i in ['n','w','s','e'] and mat[observable[i][0]][observable[i][1]] != 'w':
            x = observable[i][0]
            y = observable[i][1]
            movable[i] = observable[i]
    return movable


def find_next_move(curr, observable, explored):
    global path
    movable_dict = find_movable(observable)
    print("current:" + str(curr.location))
    # for k in movable_dict.keys():
    #     x = movable_dict[k][0]
    #     y = movable_dict[k][1]
    #     # print(movable_dict[k])
    #         print(explored[movable_dict[k]])
    #         #if explored[curr.location] < 2 and len(list_of_movable) > 1:
    #         #    list_of_movable.remove(k)
    #
    list_of_movable = sorted(movable_dict.keys(), key=lambda x: explored[movable_dict[x]])
    path += list_of_movable[0]
    return Node(curr, observable[list_of_movable[0]])


def populate_explored(explored, observable):
    for v in observable.values():
        if v not in explored:
            explored[v] = 0


def update_explored(curr, explored):
    #if deadend(curr.parent):
     #  mat[curr.parent.location[0]][curr.parent.location[1]] = 'w'
    #print("inside wpdateExplored for" + str(curr.location))
    #print("updateExplored",explored, curr.location)
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
    while goal not in observable.values():
        populate_explored(explored, observable)
        update_explored(curr, explored)
        curr = find_next_move(curr, observable, explored)
        steps += 1
        observable = surrounding_spaces(curr, len(mat))
    else:
        #print(path)
        print('Goal found')
    #last steps
    observable
    print(observable)
    print(len(explored))
    print(steps)
    print(show_exploredmap(len(mat), explored))
    return path.upper()


def show_exploredmap(length, explored):
    matrix =[[0 for _ in range(length)] for _ in range(length)]
    for k in explored.keys():
        matrix[k[0]][k[1]] = explored[k]
    for i in range(0,length):
        print(matrix[i])



if __name__ == '__main__':
    mat = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'p'],
           ['m', 'm', 's', 's', 's', 'p', 'p', 'w'],
           ['s', 's', 'p', 's', 'p', 's', 'm', 'w'],
           ['p', 'w', 'm', 's', 's', 's', 'w', 'w'],
           ['w', 'w', 'm', 'w', 'w', 'm', 'p', 'p'],
           ['w', 'p', 'w', 'w', 's', 'p', 'w', 'm'],
           ['m', 's', 's', 'w', 'w', 'p', 'p', 'p'],
           ['s', 's', 'p', 'm', 'm', 'p', 'w', 'w']]



    path = solve((6, 7), (6,2), mat)
    print(path)
