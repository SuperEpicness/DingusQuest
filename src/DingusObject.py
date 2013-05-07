#DingusQuest DQ_obj Module

import pygame, random, math

#Item class:
class DQ_obj(object):
    '''
Create a new DingusQuest Object.
    '''
    def __init__(self, x, y, objType, ID, selectable, hitRect):
        self.type = objType
        self.pos = (x, y)
        self.id = ID
        self.selectable = selectable
        self.hitRect = hitRect
        self.attributes = {}
        self.injuries = []
        self.injury_pen = 0
    
    def getPos(self):
        '''
Get the item's position.
        '''
        return self.pos
    
    def getType(self):
        '''
Get the item's type.
        '''
        return self.type
    
    def getID(self):
        '''
Get the item's identification.
        '''
        return self.id
    
    def setPos(self, x, y):
        '''
Set the item's position to the x & y coordinates given.
        '''
        self.pos = (x, y)
        
    def isSelectable(self):
        '''
See if the item can be selected.
        '''
        return self.selectable
    
    def getBlitPos(self):
        '''
Get the blit position of the item.
        '''
        return (self.pos[0], (self.pos[1]-self.type.get_height()))
    
    def intersects(self, pos, zoomFactor = 0):
        '''
See if a position intersects with the item.
        '''
        return self.getBlitRect().collidepoint(pos)
    
    def getBlitRect(self):
        '''
Get the blit Rect of the item.
        '''
        return pygame.Rect(self.getBlitPos(), (self.type.get_width(), self.type.get_height()))
    
    def getCollideRect(self):
        '''
Get the collision Rect of the item.
        '''
        if self.hitRect == None:
            return None
        return pygame.Rect((self.pos[0]+self.hitRect.left, self.pos[1]+self.hitRect.top), self.hitRect.size)
    
    def collideWith(self, other):
        '''
See if the item collides with another's item.
        '''
        def isPointInsideRect(x, y, rect):
            '''
See if a point is inside a rect.
            '''
            if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
                return True
            return False
        for a, b in [(self.getCollideRect(), other.getCollideRect()), (other.getCollideRect(), self.getCollideRect())]:
            if ((isPointInsideRect(a.left, a.top, b)) or (isPointInsideRect(a.left, a.bottom, b))
                or (isPointInsideRect(a.right, a.top, b)) or (isPointInsideRect(a.right, a.bottom, b))):
                return True
        return False

    def getAttribute(self, attribute, default = None):
        '''
Get an attribute from the DQ_obj's collection of attributes.
        '''
        try:
            return self.attributes[attribute]
        except KeyError:
            return default

    def distanceTo(self, other):
        '''
Uses the Pythagorean Theorem to find the distance between two objects.
        '''
        a = self.pos[0] - other.getPos()[0]
        b = self.pos[1] - other.getPos()[1]
        return math.sqrt(a**2 + b**2)

    def setAttribute(self, attribute, value):
        '''
Add (or update) an attribute for this DQ_obj.
        '''
        self.attributes[attribute] = value

    def appendInjury(self, Injury, location):
        self.injuries.append((Injury, location))

    def removeInjury(self, Injury, type = 'remove', default = None):
        if type == 'remove':
            try:
                self.injuries.remove(Injury)
            except ValueError:
                pass
        else:
            try:
                self.injuries.pop(Injury)
            except ValueError:
                return default

    def updateInjuryPenalty(self):
        new_injury_pen = 0
        for i in self.injuries:
            new_injury_pen += self.injuries[i].get_injury_level()
        self.injury_pen = new_injury_pen

    def get_injury_penalty(self):
        return self.injury_pen

#Injury class (say if a DQ_obj is injured in some way)
class Injury(object):
    '''
Create an Injury object.
    '''
    def __init__(self, injury_level, DQ_obj, identification, location):
        self.injurylvl = injury_level
        self.tiedto = DQ_obj
        self.id = identification
        self.location = location
        DQ_obj.appendInjury(self, location)

    def attached_to_(self, DQ_obj):
        '''
Checks if the specified DQ_obj is attached to this injury.
        '''
        return self.tiedto == DQ_obj

    def get_attached_obj(self):
        '''
Get the DQ_obj this Injury is attached to
        '''
        return self.tiedto

    def get_injury_level(self):
        '''
Get the injury level of this Injury object.
        '''
        return self.injurylvl

    def get_ID(self):
        '''
Get the identification of this object.
        '''
        return self.id

    def get_location(self):
        '''
Get the location of the Injury on the DQ_obj.
        '''
        return self.location

    def __str__(self):
        '''
Read this Injury's string mode.
        '''
        return 'Injury ' + self.id + ' is attached to DQ_obj ' + self.tiedto.getID()

#Dude class
class Dude(DQ_obj):
    '''
Create a dude.
    '''
    def __init__(self, x, y, objType, ID, selectable, hitRect):
        DQ_obj.__init__(self, x, y, objType, ID, selectable, hitRect)
        DQ_obj.setAttribute(self, 'eyesight', random.randint(25, 150))
        DQ_obj.setAttribute(self, 'agility', random.uniform(5.0, 12.5))
        DQ_obj.setAttribute(self, 'move', random.uniform(DQ_obj.getAttribute(self, 'agility') - 4, DQ_obj.getAttribute(self, 'agility') + 4))
        DQ_obj.setAttribute(self, 'endurance', random.randint(30, 150))
        DQ_obj.setAttribute(self, 'moveMode', 1)
        DQ_obj.setAttribute(self, 'endurance recovery', random.randint(1, 4))
        DQ_obj.setAttribute(self, 'skills', {})
        DQ_obj.setAttribute(self, 'strength', random.randint(6, 35))
        DQ_obj.setAttribute(self, 'stamina', random.uniform(3.0, 14.0))
        DQ_obj.setAttribute(self, 'will', random.randint(1, 10))
        DQ_obj.setAttribute(self, 'endurance', int(round((DQ_obj.getAttribute(self, 'strength') + DQ_obj.getAttribute(self, 'stamina') + DQ_obj.getAttribute(self, 'will') / 3), 0)))
        self.enduranceleft = DQ_obj.getAttribute(self, 'endurance')

    def crawl(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed/4)

    def run(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed*2)

    def sprint(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed*3)

    def jog(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed)
    
    def walk(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed/2)
    
    def climb(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed*0)

    def swim(self):
        oldSpeed = DQ_obj.getAttribute(self, 'speed')
        self.setAttribute('speed', oldSpeed*1.5)
