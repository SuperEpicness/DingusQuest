#----------DingusQuest----------
#--------------v0.5------------- (With documentation =D)
#Test Lab---Test Lab----Test Lab
#--by Simon & Daniel Struthers--

#Importing some modules:
print("Importing modules...")
import pygame, sys, math, random, easygui
from pygame.locals import * #Importing the pygame locals
from Viewport_Mod import *  #Importing the Viewport class
from DingusObject import *  #Importing the DQ_obj and Dude classes

#Comparison function:
def comp(i1, i2):
    '''
Compare two tuples to each other.
    '''
    t1 = i1.getPos()
    t2 = i2.getPos()
    if t1[1] < t2[1]:
    	return -1
    if t1[1] > t2[1]:
    	return 1
    if t1[0] > t2[0]:
    	return 1
    if t1[0] < t2[0]:
    	return -1
    return 0

#New Area function:
def newArea(size):
    '''
Create a new area given a size.
    '''
    itemList = []
    sectionSet = []
    for xx in range(worldRect.width/50):
        sectionSet.append([])
        for yy in range(worldRect.height/50):
            sectionSet[xx].append([])
    for h in range(len(natureList)):
        for i in range(int(round(natureList[h][2]*size[0]*size[1]))):
            x = random.randint(0, size[0])
            y = random.randint(0, size[1])
            itemMem = None
            if natureList[h][0] != None:
                itemMem = DQ_obj(x, y, natureImageList[h], natureList[h][0]+'('+str(x)+', '+str(y)+')', True, natureList[h][3])
            else:
                itemMem = DQ_obj(x, y, natureImageList[h], "", False, natureList[h][3])
            itemList.append(itemMem)
            CR = itemMem.getCollideRect()
            for pos in sectionFinder(itemMem, worldRect):
                sectionSet[pos[0]][pos[1]].append(itemMem)
    return itemList, sectionSet

#Items in Rectangle function:
def itemsInRect(itemList, rect):
    '''
Get a list that contains all of the items in a Rect.
    '''
    returnList = []
    for a in itemList:
        if rect.colliderect(a.getBlitRect()):
            returnList.append(a)
    return returnList

#H-scroll function:
def get_hscroll(vp):
    '''
Get the horizontal scroll value.
    '''
    if (pygame.key.get_mods() & KMOD_CTRL) :
        return vp.size[0]
    return int(vp.size[0] / 20)

#V-scroll function:
def get_vscroll(vp):
    '''
Get the vertical scroll value.
    '''
    if (pygame.key.get_mods() & KMOD_CTRL) :
        return vp.size[1]
    return int(vp.size[1] / 20)

#Center Viewport function:
def centerViewport(vp, w, pos):
    '''
Changes the values so that the viewport is centered on the position.
    '''
    vp.set_pos(pos)
    r = vp.rect()
    if r.top < w.top:
        r.top = w.top
    if r.bottom > w.bottom:
        r.bottom = w.bottom
    if r.left < w.left:
        r.left = w.left
    if r.right > w.right:
        r.right = w.right
    vp.set_pos(r.center)

#Section Finder function:
def sectionFinder(I, rect):
    '''
Returns a list of sections that contain the Rect given.
    '''
    returnValue = []
    CR = I.getCollideRect()
    if CR != None:
        if rect.collidepoint(CR.left, CR.top):
            returnValue.append((CR.left/50, CR.top/50))
        if rect.collidepoint(CR.left, CR.bottom):
            returnValue.append((CR.left/50, CR.bottom/50))
        if rect.collidepoint(CR.right, CR.bottom):
            returnValue.append((CR.right/50, CR.bottom/50))
        if rect.collidepoint(CR.right, CR.top):
            returnValue.append((CR.right/50, CR.top/50))
    return list(set(returnValue))

#Blur Surface function:
def blurSurf(surf, blur):
    '''
Blurs a surface.
    '''
    newSurf = pygame.transform.scale(surf, (int(math.ceil(surf.get_width()*blur)), int(math.ceil(surf.get_height()*blur))))
    return pygame.transform.scale(newSurf, (surf.get_width(), surf.get_height()))

#Unused Currently
# 'TinyBush1.gif', 'TinyBush2.gif', 

#User's setup:
area = ''
fillTexture = None
easygui.msgbox('''
                                                INSTRUCTIONS:

Arrow keys: scroll around the map (Hold the Ctrl key to move 1 page)

W-move up, A-move left, X-move down, D-move right, Q-upleft,
E-upright, C-downright, Z-downleft, P-pause game

Click: Select an object (Hold the Ctrl key to select multiple objects)

F-select the dude, V-center the viewport on the dude, SPACE-new map,
K-save the map, L-load a map, Esc-exit the game.
''', 'INSTRUCTIONS', 'Continue')
character = easygui.buttonbox('''
Select a character:

    1) Guy
    2) Girl
''', 'Select Character', ('Guy', 'Girl'))
if character == 'Guy':
    dude = pygame.image.load('res/Guy.gif')
else:
    dude = pygame.image.load('res/Guy1.gif')
area = easygui.choicebox('Select a landscape you want to play for this game:', 'Select Landscape',
                         ('Forest', 'Bushes', 'Classic', 'Plains', 'Urban', 'Sod Farm'))
if area == 'Forest':#name, image (gif)   ,density, collideRect settings
    natureList = [('Tree', 'res/TinyTree.gif', 0.0004, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0.0008, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0.00005, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0.00002, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0.0003, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0.0003, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/Leaves Txtre.JPG'
if area == 'Bushes':
    natureList = [('Tree', 'res/TinyTree.gif', 0.000001, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0.00002, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0.002, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0.0001, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0.0004, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0.00001, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/Grass Texture.PNG'
if area == 'Urban':
    natureList = [('Tree', 'res/TinyTree.gif', 0.00001, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0.00002, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0.00005, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0.000005, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0.00005, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0.00002, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/Seamless dirt texture.JPG'
if area == 'Plains':
    natureList = [('Tree', 'res/TinyTree.gif', 0.00001, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0.00003, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0.0003, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0.00002, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0.0001, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0.0002, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/Grass 00 seamless.JPG'
if area == 'Classic':
    natureList = [('Tree', 'res/TinyTree.gif', 0.0003, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0.0004, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0.001, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0.00003, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0.0004, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0.0002, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/Grass Texture.PNG'
if area == 'Sod Farm':
    natureList = [('Tree', 'res/TinyTree.gif', 0, pygame.Rect((5, -2), (3, 3))),
                  ('Big Tree', 'res/TinyTree1.gif', 0, pygame.Rect((7, -3), (3, 3))),
                  ('Bush', 'res/BettyBush.gif', 0, None),
                  ('Triple Bush', 'res/TinyBush.gif', 0, None),
                  ('Tiny Tree', 'res/TinyTree2.gif', 0, pygame.Rect((2, -1), (3, 3))),
                  ('Lush Tree', 'res/TinyTree3.gif', 0, pygame.Rect((7, -1), (3, 2)))]
    fillTexture = 'res/5Grass Texture.PNG'
if area == None:
    easygui.msgbox('You pressed the Cancel button! The game will now end.', '!!Cancel Button Pressed!!', 'Exit')
    raise SystemExit('Cancel-button clicked, ceasing any execution')
#Set up the pygame module and the window:
pygame.init()
pygame.font.init()
viewport = Viewport(640, 480)
worldRect = pygame.Rect((0, 0), (5000, 4000))
worldSurf = pygame.Surface((5000, 4000))
sectionSet = None
window = pygame.display.set_mode((viewport.size()[0], viewport.size()[1] + 30))
natureImageList = []
for n in natureList:
    natureImageList.append(pygame.image.load(n[1]))
itemList = []
clock = pygame.time.Clock()

#The zoom exponents: (gets raised by 2; 2 to the power of zoomExp)
zoomExp    =  0
minZoomExp =  2
maxZoomExp = -4

#Set caption for window:
pygame.display.set_caption('DingusQuest')

#Set the player's position and location:
x = random.randint(0, worldRect.right)
y = random.randint(0, worldRect.bottom)
centerViewport(viewport, worldRect, (x, y))
if character == 'Guy':
    dude = pygame.image.load('res/Guy.gif')
else:
    dude = pygame.image.load('res/Guy1.gif')
myDude = Dude(x, y, dude, "Dude", True, pygame.Rect((1, -2), (2, 2)))

#NOTE: Had to be done AFTER pygame.font.init() is called.
#Render Text function:
def render_txt(string, surf, position, font = pygame.font.Font('freesansbold.ttf', 8)):
    '''
Renders the text onto the screen given a position.
    '''
    newSurf = font.render(string, 1, (0,0,0))
    surf.blit(newSurf, position)

#Resizing function:
def resize(surf, zoomFactor = 0):
    try:
        return pygame.transform.scale(surf, (int(round((surf.get_width() / 2**zoomFactor), 0)), int(round(surf.get_height() / 2**zoomFactor, 0))))
    except ZeroDivisionError:
        return surf

#Set up some more stuff...
keyHeld = None
itemList, sectionSet = newArea(worldRect.size)
memItemList = []
itemList.append(myDude)
diagVal = math.sqrt(0.5)
dest = None
selected = []
clicked = None
updateViewable = True
hudBottomRect = Rect((0, 480), (640, 30))

bg_texture = pygame.transform.scale(pygame.image.load(fillTexture), (77, 77))

speed = myDude.getAttribute('move')

eyesight = myDude.getAttribute('eyesight')

print("Running game...")

#Main game loop:
while True:
    moveMode = myDude.getAttribute('moveMode') #Movement Mode
    #Blitting the texture on the viewport
    viewportRect = viewport.rect()
    for t in range((viewportRect.width+76+viewportRect.left%77)/77):
        for u in range((viewportRect.height+76+viewportRect.top%77)/77):
            worldSurf.blit(bg_texture, (viewportRect.left + (t*77 - viewportRect.left%77), viewportRect.top + (u*77 - viewportRect.top%77)))
    
    #Updates the viewable items if it needs to.
    if updateViewable:
        viewableItems = itemsInRect(itemList, viewportRect)
    updateViewable = False
    viewableItems.sort(comp)
    for m in viewableItems: #Bliting the items.
        r = m.getBlitRect()
##        r = Rect((r.left - viewportRect.left, r.top - viewportRect.top), r.size)
        if m.distanceTo(myDude) > eyesight: #Blur the items that are farther away from the dude.
            blurFactor = eyesight / m.distanceTo(myDude)
            worldSurf.blit(blurSurf(m.getType(), blurFactor), r.topleft)
        else:
            worldSurf.blit(m.getType(), r.topleft)
        if m.getID() in selected:
            pygame.draw.rect(worldSurf, (255, 255, 0), r, 1)
## Press Alt-4 to see the collide rects of all the items. Press Alt-3 to comment out the bellow code.
##        otherR = m.getCollideRect()
##        if otherR != None:
##            otherR = Rect((otherR.left - viewportRect.left, otherR.top - viewportRect.top), otherR.size)
##            pygame.draw.rect(window, (0, 0, 0), otherR)
    subsurf = worldSurf.subsurface(viewportRect)
    window.blit(resize(subsurf, zoomExp), (0, 0))
    #Drawing the HUD rectangle:
    pygame.draw.rect(window, (105,105,105), hudBottomRect)
    txt = 'Objects selected: ' + str(len(selected)) + ' ' + str(selected) #Selected items string
    render_txt(txt, window, (2, 490)) #Renders the "Objects selected" text using render_txt.
    pygame.display.flip() #Update the screen.
    #Main event loop:
    for event in pygame.event.get():
        if event.type == QUIT:
            #Quit the game.
            yourSelection = easygui.buttonbox('Are you sure you want to exit the game?', 'X-Button Clicked!', ('Exit', 'Continue Game'))
            if yourSelection == 'Exit':
                pygame.quit()
                raise SystemExit("Player clicked X button, ending game.")
        elif event.type == KEYDOWN:
            #Key pressed event handler:
            keyHeld = event.key
            if event.key == K_ESCAPE:
                #Quit the game.
                yourSelection = easygui.buttonbox('Are you sure you want to exit the game?', 'Escape Key Pressed!', ('Exit', 'Continue Game'))
                if yourSelection == 'Exit':
                    pygame.quit()
                    raise SystemExit('Player pressed Escape key, ending game.')
            if event.key == K_SPACE:
                #Get a new map.
                itemList, sectionSet = newArea(worldRect.size)
                itemList.append(myDude)
                updateViewable = True
                if myDude.getID() in selected:
                    selected = [myDude.getID()]
                else:
                    selected = []
            if event.key == K_k:
                #Save the memory.
                memItemList = itemList[:]
            if event.key == K_l:
                #Load the memory.
                yourInput = ''
                if len(memItemList) > 0:
                    updateViewable = True
                    itemList = memItemList[:]
            if event.key == K_f:
                #Select (or "find") the dude.
                selected = [myDude.getID()]
            if event.key == K_UP:
                #Bring the map up a bit.
                viewport.scrollUp(get_vscroll(viewportRect), worldRect)
                updateViewable = True
            if event.key == K_DOWN:
                #Bring the map down a bit.
                viewport.scrollDown(get_vscroll(viewportRect), worldRect)
                updateViewable = True
            if event.key == K_RIGHT:
                #Bring the map right a bit.
                viewport.scrollRight(get_hscroll(viewportRect), worldRect)
                updateViewable = True
            if event.key == K_LEFT:
                #Bring the map left a bit.
                viewport.scrollLeft(get_hscroll(viewportRect), worldRect)
                updateViewable = True
            if event.key == K_v:
                #Center the viewport on the dude.
                centerViewport(viewport, worldRect, (x, y))
                updateViewable = True
            if event.key == K_p:
                #Pause the game.
                pausemsg = '''
                    GAME PAUSED

By the way, your dude's attributes are:
               speed:''' + str(speed) + '''
                        eyesight:''' + str(eyesight)
                easygui.msgbox(pausemsg, 'DingusQuest Paused', 'Unpause')
            if event.key == K_EQUALS:
                #Zoom in
                if not zoomExp == maxZoomExp:
                    zoomExp -= 1
                    viewport.zoomOut()
                    centerViewport(viewport, worldRect, viewport.center())
                    updateViewable = True
            if event.key == K_MINUS:
                #Zoom out
                if not zoomExp == minZoomExp:
                    zoomExp += 1
                    viewport.zoomIn()
                    centerViewport(viewport, worldRect, viewport.center())
                    updateViewable = True
        elif event.type == KEYUP:
            #No key pressed event handler:
            keyHeld = None
        elif event.type == MOUSEBUTTONDOWN:
            #Mouse down event handler:
            keyHeld = None
            if event.button == 3:
                dest = event.pos
                dest = (dest[0] + viewportRect.left, dest[1] + viewportRect.top)
        elif event.type == MOUSEMOTION:
            #Mouse motion event handler:
            if pygame.mouse.get_pressed()[2]:
                dest = event.pos #When you right click, the dude's location is set to that position.
        elif event.type == MOUSEBUTTONUP:
            #Mouse clicked event handler:
            keyHeld = None
            if event.button == 1:
                #Right-click event handler:
                newSelection = None
                itemListRev = itemList[:]
                itemListRev.reverse() #Reverse the item list.
                lpos = viewport.point_to_grid_pos(event.pos)
                for z in itemListRev:
                    if z.intersects(lpos):
                        newSelection = z
                        break
                if newSelection != None and newSelection.isSelectable():
                    if pygame.key.get_mods() & KMOD_CTRL:
                        if newSelection.getID() in selected:
                            #If the Ctrl key is pressed and you click a selected object, remove it from the selected items list.
                            selected.remove(newSelection.getID())
                        else:
                            #Otherwise, add it to the selected items list.
                            selected.append(newSelection.getID())
                    else:
                        #If the Ctrl key isn't pressed, replace ALL of the selected items list with the clicked item.
                        selected = [newSelection.getID()]
                elif newSelection == None:
                    if not pygame.key.get_mods() & KMOD_CTRL:
                        #If you click in the middle of nowhere, remove everything from the selected items list.
                        selected = []
    if keyHeld != None:
        if keyHeld == K_x:
            #Move the dude down.
            dest = (x, y+speed)
        if keyHeld == K_w:
            #Move the dude up.
            dest = (x, y-speed)
        if keyHeld == K_d:
            #Move the dude left.
            dest = (x+speed, y)
        if keyHeld == K_a:
            #Move the dude right.
            dest = (x-speed, y)
        if keyHeld == K_q:
            #Move the dude up-left.
            dest = (x-(diagVal*speed), y-(diagVal*speed))
        if keyHeld == K_e:
            #Move the dude up-right.
            dest = (x+(diagVal*speed), y-(diagVal*speed))
        if keyHeld == K_c:
            #Move the dude down-right.
            dest = (x+(diagVal*speed), y+(diagVal*speed))
        if keyHeld == K_z:
            #Move the dude down-left.
            dest = (x-(diagVal*speed), y+(diagVal*speed))
        if keyHeld == K_s:
            #Stop the dude from moving.
            dest = None
    if dest != None and myDude.getID() in selected: #REMEMBER: Select the dude to move him.
        oldDudePos = myDude.getPos() #Get the dude's old position
        xdiff = 0
        ydiff = 0
        if dest[0] < x:
            xdiff = -1
        elif dest[0] > x:
            xdiff = 1
        if dest[1] > y:
            ydiff = 1
        elif dest[1] < y:
            ydiff = -1
        if ydiff != 0:
            xdiff *= diagVal
        if xdiff != 0:
            ydiff *= diagVal
        x += xdiff
        y += ydiff
        myDude.setPos(x, y)
        for section in sectionFinder(myDude, worldRect):
            for Item in sectionSet[section[0]][section[1]]:
                if Item.collideWith(myDude):
                    myDude.setPos(oldDudePos[0], oldDudePos[1])
                    x -= xdiff
                    y -= ydiff
                    break
    #Tick the clock:
    clock.tick(40)
