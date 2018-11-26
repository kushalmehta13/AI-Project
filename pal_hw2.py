""""
Created by: Ajay Shivchandra Pal
"""
"""
[1] references: https://docs.python.org/2/library -- for various library functions -abs(), random()
[2] https://stackoverflow.com/questions/3282823/get-the-key-corresponding-to-the-minimum-value-within-a-dictionary -- getting the minimu value from the dictionary
[3] https://stackoverflow.com/questions/5384914/how-to-delete-items-from-a-dictionary-while-iterating-over-it -- deleting the values in dictionary
"""
import random

class Node:
    """
    Data Structure that holds the state value for different blocks in the python.
    """
    def __init__(self):
        #position on the squre space
        self.x = (0, 0)
        #total cost so far for the node
        self.gn = 0
        #heuristic cost for the node
        self.hn = 0
        #parent node for the current node
        self.parent = None

def hn(position, goal):
    """
    Calculates the heuristic for the position.
    hn(position) = straight line distance
    :param position: tuple having x,y value
    :param goal: tuple having x,y value of goal position
    :return: integer denoting heuristic cost
    """
    #distance
    d = 0
    if isinstance(position, tuple) and isinstance(goal, tuple):
        (x1, y1), (x2, y2) = position, goal
        d = abs(x1-x2) + abs(y1-y2) #manhatten distance
    return d


def is_goal(goal_node, current_node):
    """
    :param goal_node: the Goal Node Tuple
    :param current_node: Current Node Tuple
    :return: True if the current node is goal , False otherwise
    """
    if goal_node[0] == current_node[0] and goal_node[1] == current_node[1]:
        return True
    return False


def gen_append_child(parent_node, world, visited, goal, frontier):
    """
       generating valid children for the current node and then adding it to the frontier
       :param: current node whose childs needs to be generated
       :param: world: N*N matrix
       :param: visited: list of visited node
       :param: goal : goal node

    """
    terrain_type_cost = {"m": 100, "p": 10, "s": 30}
    x, y = parent_node.x
    limit = len(world)
    allowed_moves = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    for p in allowed_moves:
        if p[0] >= limit or p[1] >= limit or p[0] < 0 or p[1] < 0: #as the moving outside of space is not allowed
            continue
        else:
            if p not in visited:
                new_node = Node()
                new_node.x = p
                new_node.gn = terrain_type_cost[world[p[0]][p[1]]] + parent_node.gn
                new_node.hn = hn(p, goal)
                new_node.parent = parent_node
                if new_node.x not in frontier:
                    frontier[new_node.x] = new_node
                elif new_node.gn + new_node.hn < frontier[new_node.x].gn + frontier[new_node.x].hn:
                    frontier[new_node.x] = new_node
    return frontier


def remove_node_from_frontier(frontier, current_goal_cost, visited):
    """
    this methods removes the node from frontier whose cost is more than current goal node
    :param frontier: all the node that needs to be explored
    :param current_goal_cost: currently available goal cost
    :return: frontier with all the nodes removed whose cost is more than goal cost
    """
    delete = []
    for i in frontier:
        if frontier[i].gn > current_goal_cost:
            delete.append(i)
    for i in delete:
        visited[frontier[i].x] = frontier[i]
        del frontier[i]

    return (frontier, visited)


def convert_points_to_directions(node):
    """
    Converting the point to point travel in S, E, W, N String.
    e.g. if agent is travelling from 0,1 -> 0,2 the method will return E.
    :param node: A goal node which needs to be travelled back
    :return: returns the String containing directions
    """
    map = {(1, 0): 'N', (0, -1): 'E', (-1, 0): 'S', (0, 1): 'W'}
    point1 = node
    point2 = node.parent
    instructions = [];
    while point2:
        x = point2.x[0] - point1.x[0]
        y = point2.x[1] - point1.x[1]
        instructions.append(map[(x, y)])
        point2 = point2.parent
        point1 = point1.parent

    inst_str = ""
    for x in instructions:
        inst_str = x + inst_str
    return inst_str


def solve(start, goal, world):
    """
    :param start: (x,y) tuple, representing start position for search problem
    :param goal: (x',y') tuple, representing goal position for search problem
    :param world: N*N matrix having 'm','p','s' characters.
    :return: Path String containing (N, S, E, W) character representing North, South, East and West, which will lead to goal state.
    """
    #dictionary of visited points on square space.
    visited = {}
    #dictionary of nodes ready to explore
    frontier = {}
    #initializing the start Node
    l = len(world)
    if not (0 <= start[0] < l and 0 <= start[1] < l and 0 <= goal[0]< l and 0 <= goal[1] < l):
        return ""

    start_node = Node()
    start_node.x = start
    start_node.gn = 0
    start_node.hn = hn(start, goal)
    frontier[start_node.x] = start_node

    while len(frontier) > 0:
        current_node = frontier.pop(min(frontier, key=lambda k: frontier[k].gn + frontier[k].hn))
        if is_goal(goal, current_node.x):
            break
        else:
            visited[current_node.x] = current_node
            frontier = gen_append_child(current_node, world, visited, goal, frontier)

    return convert_points_to_directions(current_node)


# def generate_world(limit):
#     """
#     Generates random matrix, goal and start for given limit.
#     :param limit: any number
#     :return: the world, start, and goal.
#     """
#
#     dimension = random.randint(2, limit)
#     world = [[None]*dimension for i in range(dimension)]
#
#     #choosing start and goal state in mountain
#     goal = (random.randint(0, dimension-1),random.randint(0, dimension-1))
#     start = (random.randint(0, dimension-1),random.randint(0, dimension-1))
#
#     #putting p,s,m in the world
#     types = ['p','s','m']
#     for i in range(dimension):
#         for j in range(dimension):
#             world[i][j] = random.choice(types)
#
#     return world, start, goal
#
#
# i = []
# i.append([[['m', 'm', 'm', 's'], ['m', 'm', 'm', 's'],['m', 'm', 'm', 's'], ['p', 'p', 'p', 'p']], (0, 0), (2, 2)])
# i.append([[['p', 'p', 'p'], ['p', 'm', 'p'], ['s', 's', 's']], (1,0), (2, 2)])
#
# for x in range(0, len(i)):
#     solution = solve(i[x][1], i[x][2], i[x][0])
#     print(solution)
#     print()
#

