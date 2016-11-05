import tkinter as tk
# This knows about pixels

# Some colours
BGC = '#ff0ff0ff0'
FGC = '#000000000'
WKC = '#000fc0fc0'
VSC = '#0000000cf'
RRR = '#fff000000'
GGG = '#000fff000'
BBB = '#000000fff'
XXX = '#0ff0ff000'
LGB = '#8f08f0fff'

# Room size
ROOM_HEIGHT_IN_PIX = 16
ROOM_WIDTH_IN_PIX = 16

# Wall-IDs
U_WALL = 1
R_WALL = 2
D_WALL = 4
L_WALL = 8

# Maze 'margins'
x_offset = 16
y_offset = 16

class MazeGraphics(object):
    DEBUG = 0
    roomheight = ROOM_HEIGHT_IN_PIX
    roomwidth = ROOM_WIDTH_IN_PIX
    walker = (0, 0) # The maze-walker
    mz = [] # The maze representation
    
    class Room(object):
        # Maze room
        def __init__(self, field, loc, width, height):
            self.field = field
            # corner points and center point
            self.loc = loc
            x0, y0 = loc # upper left
            self.ld = (x0 + width, y0) # upper right
            self.ru = (x0, y0 + height) # lower left
            self.rd = (x0 + width, y0 + height) # lower right
            self.center = (x0 + width//2, y0 + height//2)
            # walls
            x1, y1 = self.ru
            x2, y2 = self.rd
            x3, y3 = self.ld
            self.uw = field.create_line(y0, x0, y1, x1, fill=FGC, disabledfill=BGC)
            self.rw = field.create_line(y1, x1, y2, x2, fill=FGC, disabledfill=BGC)
            self.dw = field.create_line(y2, x2, y3, x3, fill=FGC, disabledfill=BGC)
            self.lw = field.create_line(y3, x3, y0, x0, fill=FGC, disabledfill=BGC)
            # walker
            x0 += 2
            y0 += 2
            x2 -= 2
            y2 -= 2
            self.wlk = field.create_oval(y0, x0, y2, x2, fill=BGC, disabledfill=BGC, outline=BGC)

        def clear(self):
            self.field.itemconfigure(self.uw, fill=FGC)
            self.field.itemconfigure(self.rw, fill=FGC)
            self.field.itemconfigure(self.dw, fill=FGC)
            self.field.itemconfigure(self.lw, fill=FGC)
            self.field.itemconfigure(self.wlk, fill=BGC)

        def setWalker(self):
            self.field.itemconfigure(self.wlk, fill=BBB)

        def clearWalker(self):
            self.field.itemconfigure(self.wlk, fill=BGC)

        def markWalker(self):
            self.field.itemconfigure(self.wlk, fill=LGB)

        def markVisited(self):
            # for debugging
            self.field.itemconfigure(self.wlk, fill=VSC)
            
        def breakWall(self, wall):
            if wall == U_WALL:
                #self.field.itemconfigure(self.uw, width=4)
                self.field.itemconfigure(self.uw, fill=BGC)
            elif wall == R_WALL:
                #self.field.itemconfigure(self.rw, width=4)
                self.field.itemconfigure(self.rw, fill=BGC)
            elif wall == D_WALL:
                #self.field.itemconfigure(self.dw, width=4)
                self.field.itemconfigure(self.dw, fill=BGC)
            elif wall == L_WALL:
                #self.field.itemconfigure(self.lw, width=4)
                self.field.itemconfigure(self.lw, fill=BGC)
                
        def markCell(self, color):
            self.field.itemconfigure(self.wlk, fill=color)
            #pass
            
    def __init__(self, field, x, y):
        self.field = field
        self.width = y
        self.height = x
        # build the maze array of rooms
        for i in range(0, x):
            self.mz.append([])
            for j in range(0, y):
                loc = (i*self.roomheight+x_offset, j*self.roomwidth+y_offset)
                rm = self.Room(field, loc, self.roomwidth, self.roomheight)
                self.mz[i].append(rm)

    def clear(self):
        # reset the maze to init state
        x, y = self.walker
        self.mz[x][y].clearWalker()
        self.walker = (0,0)
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.mz[i][j].clear()

    def breakWall(self, x, y, w):
        # Make the entry and exit places
        if w == 'U':
            self.mz[x][y].breakWall(U_WALL)
        else:
            self.mz[x][y].breakWall(D_WALL)
            
    def connectRooms(self, x, y, x1, y1):
        # Break the walls between two rooms
        if x == x1:
            if y < y1:
                if self.DEBUG != 0:
                    self.mz[x][y].markCell('#ff0000000')
                    self.mz[x1][y1].markCell('#ff0000000')
                    print("Connect rooms: (",x,",",y,") R_WALL and (",x1,",",y1,") L_WALL")
                self.mz[x][y].breakWall(R_WALL)
                self.mz[x1][y1].breakWall(L_WALL)
            else:
                if self.DEBUG != 0:
                    self.mz[x][y].markCell('#ff0000000')
                    self.mz[x1][y1].markCell('#ff0000000')
                    print("Connect rooms: (",x,",",y,") L_WALL and (",x1,",",y1,") R_WALL")
                self.mz[x][y].breakWall(L_WALL)
                self.mz[x1][y1].breakWall(R_WALL)
        else:
            if x < x1:
                if self.DEBUG != 0:
                    self.mz[x][y].markCell('#ff0000000')
                    self.mz[x1][y1].markCell('#ff0000000')
                    print("Connect rooms: (",x,",",y,") D_WALL and (",x1,",",y1,") U_WALL")
                self.mz[x][y].breakWall(D_WALL)
                self.mz[x1][y1].breakWall(U_WALL)
            else:
                if self.DEBUG != 0:
                    self.mz[x][y].markCell('#ff0000000')
                    self.mz[x1][y1].markCell('#ff0000000')
                    print("Connect rooms: (",x,",",y,") U_WALL and (",x1,",",y1,") D_WALL")
                self.mz[x][y].breakWall(U_WALL)
                self.mz[x1][y1].breakWall(D_WALL)            

    def clearWalker(self, i, j):
        self.mz[i][j].clearWalker()
        
    def setGoal(self, i, j):
        # Make exit place more visible
        self.mz[i][j].markCell(RRR)

    def setWalker(self, i, j):
        # Move walker from a room to another
        x, y = self.walker
        #print("graph: walker = ", self.walker, " to ", (i ,j))
        self.mz[x][y].clearWalker()
        self.mz[i][j].setWalker()
        self.walker = (i, j)
        
    def moveWalker(self, i, j):
        # Move walker from a room to another leaving a trace
        x, y = self.walker
        #print("graph: walker = ", self.walker, " to ", (i ,j))
        #self.mz[x][y].clearWalker()
        self.mz[x][y].markWalker()
        self.mz[i][j].setWalker()
        self.walker = (i, j)
       
