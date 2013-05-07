#DingusQuest World Module

import pygame, random

class World(object):
    '''
Define a brand new 5000x4000 world.
    '''
    def __init__(self):
        self.width = 5000
        self.height= 4000
        self.worldSurf = pygame.Surface((self.width, self.height))
    
    def randomPos(self):
        '''
Get a random position in the world.
        '''
        return (random.randint(0, self.width), random.randint(0, self.height))
    
    def pathTo(self, Dude, pos):
        '''
Returns a list of positions and a list of tuples of a movement type and the cost for it.
        '''
        lst = [[], []]
        
    def getSubsurf(self, DQ_obj):
        '''
Get a subsurface of the world according to a DQ_obj.
        '''
        return
