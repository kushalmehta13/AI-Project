from agent import BaseAgent
import utils
import util_functions

class DcrawlerAgent2(BaseAgent):
    """
   A Dcrawler agent that moves in each direction based on score value of each options
   ----------
   height: int
       Height of the game map
   width: int
       Width of the game map
   initial_strength: int
       Initial strength of the agent
   name: str
       Name of the agent
   """

    def __init__(self, height, width, initial_strength, name='decrawler_agent2'):
        super().__init__(height=height, width=width,initial_strength=initial_strength, name=name)
        self.location = tuple() # for storing the current location
        self.game_map = None #for storing the game map
        self.map_objects = dict() # for keeping track of map_objects
        self.explored = dict() # for keeping track of explored states
        self.init_explored()
        self.path =""

    def init_explored(self):
        # self.dir_explored = {utils.Directions.N:self.height/2,utils.Directions.S:self.height/2,utils.Directions.E:self.width/2,utils.Directions.W:self.width/2}
        for i in range(self.height):
            for j in range(self.width):
                self.explored[(i,j)] = 0


    def check_dir_explored(self):

        h = self.location[0]
        w = self.location[1]
        dir_explored = {utils.Directions.N:0,utils.Directions.S:0,utils.Directions.E:0,utils.Directions.W:0}
        for i in range(h):
            for j in range(w):
                if(self.game_map[i][j] == utils.MapTiles.U):
                    if i <= h/2:
                        dir_explored[utils.Directions.N]+=1
                    else:
                        dir_explored[utils.Directions.S]+=1

                    if j <= w/2:
                        dir_explored[utils.Directions.W]+=1
                    else:
                        dir_explored[utils.Directions.E]+=1
        return dir_explored


    def update_explored_info(self, location):
        """
        keeps track of visited tiles by maintaining the number of visit for the particular tile in explored dictionary
        :param location: current location in the form of integer tuple
        :return: Nothing
        """
        #self.update_direction_explored_count(location)

        if location in self.explored:
            self.explored[location] += 1
        else:
            self.explored[location] = 1


    def get_location(self, dir, location):
        """
        returns the location of the next tile in specified direction
        :param dir:  direction
        :param location: current location
        :return: tuple (x,y) - next tile location if agents moved in direction dir
        """
        dir_location = {utils.Directions.NORTH:(-1,0), utils.Directions.SOUTH:(1,0), utils.Directions.EAST:(0,1), utils.Directions.WEST:(0,-1)}

        x_incr, y_incr = dir_location[dir]
        new_loc = (location[0]+ x_incr, location[1]+y_incr)
        return new_loc

    def is_Object_present(self,type):
        for obj in self.map_objects:
            if isinstance(obj, type):
                return True

    def get_movable(self, loc):
        """
        This method finds which moves the agent can actually take from the current location and returns the possible direction
        in which agent can move

        :return: movable dictionary containing direction in which agent can travel with score value.
        """
        x = loc[0]
        y = loc[1]
        movable = dict()

        # North Neighbor
        if x-1 >= 0 and self.game_map[x-1][y] != utils.MapTiles.W:
            loc = (x-1, y)
            movable[loc] = utils.Directions.N
        # East Neighbor
        if y+1 <= self.width - 1 and self.game_map[x][y+1] != utils.MapTiles.W:
            loc = (x, y+1)
            movable[loc] = utils.Directions.E
        # South Neighbor
        if x+1 <= self.height - 1 and self.game_map[x+1][y] != utils.MapTiles.W:
            loc = (x+1, y)
            movable[loc] = utils.Directions.S
        # West Neighbor
        if y-1 >= 0 and self.game_map[x][y-1] != utils.MapTiles.W:
            loc = (x, y-1)
            movable[loc] = utils.Directions.W

        return movable

    def decision_maker(self, movable):
        """
        :param movable: dictionary of possible moves along with score for each move
        :return: returns the best direction that is less visited and has highest score value.
        """

        minimum = self.explored[min(movable.keys(), key = lambda x : self.explored[x])]
        keys = [v for v in movable.keys() if self.explored[v] == minimum]

        if len(keys) == 1:
            return movable[keys[0]]
        else:
            dir_explored = self.check_dir_explored()
            dir = movable[max(keys, key = lambda x: dir_explored[movable[x]])]

            return dir

    def step(self, location, strength, game_map, map_objects):
        self.location = location
        self.strength = strength
        self.game_map = game_map
        self.map_objects = map_objects
        # adding current locations to explored with count = 1

        self.update_explored_info(location)
        # finding the possible movable directions from current location
        movable = self.get_movable(location)
        # finding the best direction among the movable directions found above
        dir = self.decision_maker(movable)
        #input()
        # directions ->
        dir_dict = {utils.Directions.N:'N', utils.Directions.E:'E', utils.Directions.S:'S', utils.Directions.W:'W'}
        self.path += dir_dict[dir]

        return dir


    def show_explored(self):
        print("----------------------------------------------------------------")
        mat= [[0 for i in range(self.height)] for j in range(self.width)]
        dict = {utils.MapTiles.MOUNTAIN : 'W'}
        for i,j in self.explored.keys():
            mat[i][j] = self.explored[(i,j)]

        row = '  '
        for i in range(len(mat)):
            row += str(i) + ' '
        print(row)
        for i in range(len(mat)):
            row = str(i)+" "
            for j in range(len(mat[i])):
                row += str(mat[i][j])
                row += ' '
            print(row)
