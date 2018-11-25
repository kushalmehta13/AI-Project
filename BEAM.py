import heapq
import math
import random
from collections import Counter

cost_dict = {'w' : math.inf, 'm' : 100, 'p' : 10, 's' : 30}
mat = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'p'],
       ['m', 'm', 's', 's', 's', 'p', 'p', 'w'],
       ['s', 's', 'p', 's', 'p', 's', 'm', 'w'],
       ['p', 'w', 'm', 's', 's', 's', 'w', 'w'],
       ['w', 'w', 'm', 'w', 'w', 'm', 'p', 'p'],
       ['w', 'p', 'w', 'w', 's', 'p', 'w', 'm'],
       ['m', 's', 's', 'w', 'w', 'p', 'p', 'p'],
       ['s', 's', 'p', 'm', 'm', 'p', 'w', 'w']]

class Node():

    def __init__(self, parent = None, location = None):
        self.parent = parent
        self.location = location

        # cost function
        self.f = 0
        # Heuristic
        self.h = 0
        self.g = self.f + self.h

def goalTest(curr, goal):
    if curr == goal:
        return True
    return False


def getTile(observable, direction):
    return mat[observable[direction][0]][observable[direction][1]]

def surrounding_spaces(curr, mat):
    # Check if the agent is near the border of the maze
    x = curr.location[0]
    y = curr.location[1]
    observable = {}
    # North Neighbor
    if x-1 >= 0:
        observable['n'] = (x-1, y)
    # East Neighbor
    if y+1 <= len(mat) - 1:
        observable['e'] = (x, y+1)
    # South Neighbor
    if x+1 <= len(mat) - 1:
        observable['s'] = (x+1,y)
    # West Neighbor
    if y-1 >= 0:
        observable['w'] = (x, y-1)
    # North east neighbor
    if x-1 >= 0 and y+1 <= len(mat) - 1 and not (getTile(observable, 'n') == getTile(observable, 'e') == 'w'):
        observable['ne'] = (x-1, y+1)
    # South East Neighbor
    if x+1 <= len(mat) - 1 and y+1 <= len(mat) - 1 and not (getTile(observable, 's') == getTile(observable, 'e') == 'w'):
        observable['se'] = (x+1, y+1)
    # South West Neighbor
    if x+1 <= len(mat) - 1 and y-1 >= 0 and not (getTile(observable, 's') == getTile(observable, 'w') == 'w'):
        observable['sw'] = (x+1, y-1)
    # North West Neighbor
    if x-1 >= 0 and y-1 >= 0 and not (getTile(observable, 'n') == getTile(observable, 'w') == 'w'):
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

def findNextMove(curr, observable, explored):
    # dir = ''
    # if curr.parent:
    #     ref = {(0, 1): 'e', (0, -1): 'w', (-1, 0): 'n', (1, 0): 's'}
    #     loc1 = curr.location
    #     loc2 = curr.parent.location
    #     diff = (loc1[0] - loc2[0], loc1[1] - loc2[1])
    #     dir = ref[diff]
        #
        # unexplored = []
        # x = curr.location[0]
        # y = curr.location[1]
        # for k, v in explored.items():
        #     diff = (k[0]-x,k[1]-y)
        #     if v == 0 and (k[0]-x == 0 or k[1]-y ==0) and k!=(x,y) and getTile(observable, ref[diff])!='w':
        #         unexplored.append(k)
        # if len(unexplored) > 0:
        #     return Node(curr, random.choice(unexplored))

    movable_dict = find_movable(observable)
    print("current:" + str(curr.location))
    list_of_movable = sorted(movable_dict.keys(), key=lambda x: explored[movable_dict[x]])
    print(list_of_movable)
    # for k in movable_dict.keys():
    #     x = movable_dict[k][0]
    #     y = movable_dict[k][1]
    #     # print(movable_dict[k])
    #     # print(x + 1 >= len(mat), x - 1 <= 0 , y - 1 <= 0,
    #     #       y + 1 >= len(mat))
    #     if (x+1 >= len(mat) or x-1 <= 0 or y-1 <= 0 or y+1 >= len(mat)):
    #         print(explored[movable_dict[k]])
    #         if explored[curr.location] < 2 and len(list_of_movable) > 1:
    #             list_of_movable.remove(k)

    #print(list_of_movable)

    #
    # if dir in observable and getTile(observable, dir) != 'w' and explored[observable[dir]] != 2:
    #     return Node(curr, observable[dir])

    return Node(curr, observable[list_of_movable[0]])


    # # check for zero
    # if 'n' in observable and explored[observable['n']] == 0 and getTile(observable, 'n') != 'w':
    #     return Node(curr, observable['n'])
    # elif 'e' in observable and explored[observable['e']] == 0 and getTile(observable, 'e') != 'w':
    #     return Node(curr, observable['e'])
    # elif 's' in observable and explored[observable['s']] == 0 and getTile(observable, 's') != 'w':
    #     return Node(curr, observable['s'])
    # elif 'w' in observable and explored[observable['w']] == 0 and getTile(observable, 'w') != 'w':
    #     return Node(curr, observable['w'])


    # #     go west if possible
    # elif 'w' in observable and getTile(observable, 'w') != 'w' and explored[observable['w']] != 2:
    #     return Node(curr, observable['w'])
    # #      go north if possible
    # elif 'n' in observable and getTile(observable, 'n') != 'w' and explored[observable['n']] != 2:
    #     return Node(curr, observable['n'])
    # #   go east if possible
    # elif 'e' in observable and getTile(observable, 'e') != 'w' and explored[observable['e']] != 2:
    #     return Node(curr, observable['e'])
    # #     go south if possible
    # elif 's' in observable and getTile(observable, 's') != 'w' and explored[observable['s']] != 2:
    #     return Node(curr, observable['s'])



def populateExplored(explored, observable):
    for v in observable.values():
        if v not in explored:
            explored[v] = 0

def deadend(par):
    o = surrounding_spaces(par, mat)
    count = 0
    if 'e' in o and getTile(o, 'e') == 'w':
        count+=1
    if 'w' in o and getTile(o, 'w') == 'w':
        count += 1
    if 'n' in o and getTile(o, 'n') == 'w':
        count += 1
    if 's' in o and getTile(o, 's') == 'w':
        count += 1

    if count == 3:
        return True

    return False


def updateExplored(curr, explored):
    #if deadend(curr.parent):
     #  mat[curr.parent.location[0]][curr.parent.location[1]] = 'w'
    #print("inside wpdateExplored for" + str(curr.location))
    print("updateExplored",explored, curr.location)
    explored[curr.location] += 1


def solve(start, goal, mat):
    startNode = Node(None, start)  # ref = {(0, 1): 'e', (0, -1): 'w', (-1, 0): 'n', (1, 0): 's'}
        # loc1 = curr.location
        # loc2 = curr.parent.location
        # diff = (loc1[0] - loc2[0], loc1[1] - loc2[1])
        # dir =ref[diff]e(None, start)
    endNode = Node(None, goal)
    curr = startNode
    observable = surrounding_spaces(curr, mat)
    explored = {}
    # traversed = []
    explored[startNode.location] = 0
    # print(observable)
    steps = 0
    while (goal not in observable.values()):
        populateExplored(explored, observable)
        updateExplored(curr, explored)
        curr = findNextMove(curr, observable, explored)
        #print(curr.location)
        #input()
        steps+=1
        observable = surrounding_spaces(curr, mat)
    else:
        print('Goal found')
    #     observable = surrounding_spaces(curr, mat)
    #     chosenTile = findNextMove(observable, mat, curr)
    print(steps)

if __name__ == '__main__':
    path = solve((6,7), (2,3), mat)
