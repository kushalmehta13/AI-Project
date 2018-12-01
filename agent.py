import numpy as np
#from utils import Directions, MapTiles, MapObject, PowerUp, StaticMonster, MapTiles, tile_cost
import utils

# import MEHTA_hw4

class BaseAgent(object):
    def __init__(self, name='base_agent'):
        """

        Parameters
        ----------
        name: str
            Name of the agent
        """
        self.name = name

    def step(self, location, strength, game_map, map_objects):
        """

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far


        Returns
        -------
        direction: Directions
            Which direction to move
        """
        pass


class RandomAgent(BaseAgent):

    def __init__(self, name='random_agent'):
        return super().__init__(name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        return np.random.choice(list(Directions))

class Dcrawler(BaseAgent):
    class ExploredStates:
        def __init__(self, tile, obj, count):
            self.tile = tile
            self.obj = obj
            self.count = count
    location = tuple()
    strength = int()
    game_map = dict()
    map_objects = dict()
    explored = dict()
    def __init__(self, name='dcrawler'):
        location = tuple()
        return super().__init__(name=name)
    #
    # def chooseBestTile(self, movable):
    #     # objs[0] is game_map
    #     # objs[1] is map_objects
    #     for dir, objs in movable:
    #
    #     return

    def score(self, loc):
        return_value = 0
        #tc = self.game_map[loc]

        if loc in self.map_objects:
            obj = self.map_objects[loc]
            if isinstance(obj, utils.PowerUp):
                return_value =  obj.delta - utils.tile_cost[self.game_map[loc]]
            elif isinstance(obj, utils.StaticMonster)   :
                win_chance = (self.strength - utils.tile_cost[self.game_map[loc]])/((self.strength - utils.tile_cost[self.game_map[loc]]) + obj.strength)
                if(win_chance > 0.5):
                    return_value = obj.strength - utils.tile_cost[self.game_map[loc]]
                else:
                    return_value = obj.delta - utils.tile_cost[self.game_map[loc]]
        else:
            # print("%%%%%%%%%%%%%",loc)
            # print("%%%%%%%%%%", self.game_map.shape)
            return_value= -utils.tile_cost[self.game_map[loc]]
        return return_value

    def get_movable(self):
        '''
        location: tuple <int, int>
        game_map: dict <map: value>
        Returns: dict <direction (string) : location>
        '''
        x = self.location[0]
        y = self.location[1]
        movable = dict()
        maxlen = len(self.game_map)
        print(self.game_map[x-1][y])
        # North Neighbor
        if x-1 >= 0 and self.game_map[x-1][y] != utils.MapTiles.W:
            loc = (x-1, y)
            movable[utils.Directions.N] = self.score(loc)
            self.explored[loc] =  Dcrawler.ExploredStates(self.game_map[loc], self.map_objects[loc] if (loc in self.map_objects) else None, 0)
        # East Neighbor
        if y+1 <= maxlen - 1 and self.game_map[x][y+1] != utils.MapTiles.W:
            loc = (x, y+1)
            movable[utils.Directions.E] = self.score(loc)
            self.explored[loc] =  Dcrawler.ExploredStates(self.game_map[loc], self.map_objects[loc] if (loc in self.map_objects) else None, 0)
        # South Neighbor
        if x+1 <= maxlen - 1 and self.game_map[x+1][y] != utils.MapTiles.W:
            loc = (x+1, y)
            movable[utils.Directions.S] = self.score(loc)
            self.explored[loc] =  Dcrawler.ExploredStates(self.game_map[loc], self.map_objects[loc] if loc in self.map_objects else None, 0)
        # West Neighbor
        if y-1 >= 0 and self.game_map[x][y-1] != utils.MapTiles.W:
            loc = (x, y-1)
            movable[utils.Directions.W] = self.score(loc)
            self.explored[loc] = Dcrawler.ExploredStates(self.game_map[loc], self.map_objects[loc] if loc in self.map_objects else None, 0)

        return movable


    def step(self, location, strength, game_map, map_objects):
        self.location = location
        self.strength = strength
        self.game_map = game_map
        self.map_objects = map_objects

        movable = self.get_movable()
        if location in self.explored:
            self.explored[location].count+=1
        else:
            self.explored[location] = Dcrawler.ExploredStates(game_map[location], map_objects[location] if (location in map_objects) else None, 0)
        dir = max(movable, key = lambda k :movable[k])

        return dir
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        # solve(location, )

        # return np.random.choice(list(Directions))