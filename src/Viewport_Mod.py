#DingusQuest Viewport Module

import pygame

class Viewport(object):
    '''
Create a viewport.
    '''
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.zoom = 0
        self.c = (width/2, height/2)

    def zoomIn(self):
        '''
Zoom in one zoom level.
        '''
        self.zoom += 1

    def zoomOut(self):
        '''
Zoom out one zoom level.
        '''
        self.zoom -= 1

    def width(self):
        return int((self.w * (2**self.zoom)) + 0.5)

    def height(self):
        return int((self.h * (2**self.zoom)) + 0.5)

    def center(self):
        return self.c

    def set_pos(self, pos):
        self.c = pos

    def set_zoom(self, newzoom):
        self.zoom = newzoom

    def size(self):
        return (self.width(), self.height())

    def top(self):
        return self.c[1] - (self.height()/2)

    def left(self):
        return self.c[0] - (self.width()/2)

    def bottom(self):
        return self.top() + self.height()

    def right(self):
        return self.left() + self.width()
    
    def topleft(self):
        return (self.top(), self.left())

    def bottomright(self):
        return (self.bottom(), self.right())

    def rect(self):
        '''
Get the complete Rect of the viewport.
        '''
        return pygame.Rect(self.left(), self.top(), self.width(), self.height())

    def scrollUp(self, py, rect):
        '''
Make the viewport scroll up.
        '''
        y = self.top() - py
        if (y < rect.top):
            y = rect.top
        y += (self.height()/2)
        self.c = (self.c[0], y)

    def scrollDown(self, py, rect):
        '''
Make the viewport scroll down.
        '''
        y = self.bottom() + py
        if (y > rect.bottom):
            y = rect.bottom
        y -= (self.height()/2)
        self.c = (self.c[0], y)

    def scrollLeft(self, px, rect):
        x = self.left() - px
        if (x < rect.left):
            x = rect.left
        x += (self.width()/2)
        self.c = (x, self.c[1])

    def scrollRight(self, px, rect):
        x = self.right() + px
        if (x > rect.right):
            x = rect.right
        x -= (self.width()/2)
        self.c = (x, self.c[1])

    def __str__(self):
        '''
Prints out the viewport's Rect.
        '''
        return pygame.Rect.__str__(self.rect())

    def point_to_grid_pos(self, pos):
        '''
When you click at a certain spot, this will translate it into a grid position.
        '''
        return (int((pos[0] * 2**self.zoom)) + self.left(), int((pos[1] * 2**self.zoom) + self.top()))

