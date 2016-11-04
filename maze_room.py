
U_WALL = 1
R_WALL = 2
D_WALL = 4
L_WALL = 8
ALL_WALLS = 15
FRONT = 16
VISITED = 32

class MazeRoom(object):
    room = None
    def __init__(self):
        self.room = ALL_WALLS

    def clear(self):
        self.room = ALL_WALLS

    def breakWall(self, wall):
        self.room &= ~wall

    def hasWall(self, wall):
        if self.room & wall == 0:
            return False
        else:
            return True

    def visit(self):
        self.room |= VISITED

    def visited(self):
        if self.room & VISITED == 0:
            return False
        else:
            return True
        
    def setFront(self):
        self.room |= FRONT

    def isFront(self):
        if self.room & FRONT == 0:
            return False
        else:
            return True

    def getRoom(self):
        return self.room
