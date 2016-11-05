# The maze game logic
import tkinter as tk
from tkinter import messagebox
import random
import maze_room
import maze_graphics

class MazeGame(object):
    DEBUG = 0
    mz = []
    class RoomSet(object):
        # A helper - 'ordered' set with random pop
        def __init__(self):
            self.coll = []
        
        def add(self, item):
            if item not in self.coll:
                self.coll.append(item)

        def pop(self):
            #print(self.coll)
            rnd = random.randint(0, len(self.coll) - 1)
            #item = self.coll[rnd]
            item = self.coll.pop(rnd)
            return item
        
        def len(self):
            return len(self.coll)
        
        def clear(self):
            # Remove all elements
            self.coll.clear()

    def __init__(self, field, x, y):
        self.field_height = x
        self.field_width = y
        self.walker = (0,0)
        self.field = field
        # Build maze - array of rooms
        # self.mz = [[0]*width for i in range(height)]
        for i in range(0, x):
            self.mz.append([]) # add a row
            for j in range(0, y):
                rm = maze_room.MazeRoom()
                self.mz[i].append(rm) # add room (column) to a row
        # Create maze representation
        self.disp = maze_graphics.MazeGraphics(field, x, y)

    def clearGame(self):
        # Clears the game
        self.walker = (0,0)
        self.disp.setWalker(0, 0)
        self.disp.clear()
        for i in range(0, self.field_height):
            for j in range(0, self.field_width):
                self.mz[i][j].clear()

    def addToFront(self, front, room):
        # Adds the neighbouring non-visited rooms to the front set
        r, c = room
        if r != 0:
            if self.mz[r - 1][c].visited() == False:
                front.add((r - 1, c))
        if r != self.field_height - 1:
            if self.mz[r + 1][c].visited() == False:
                front.add((r + 1, c))
        if c != 0:
            if self.mz[r][c - 1].visited() == False:
                front.add((r, c - 1))
        if c != self.field_width - 1:
            if self.mz[r][c + 1].visited() == False:
                front.add((r, c + 1))
        return front

    def breakWall(self, r, c):
        # Selects one of the possible walls and breaks it (from both sides)
        # Gets a front room coordinates as parameters

        # Create a set of possible walls to break
        # A breakable wall ii suck that separates a visited and front room
        breakable = self.RoomSet()
        if r != 0:
            if self.mz[r - 1][c].visited():
                breakable.add((r - 1, c))
        if r != self.field_height - 1:
            if self.mz[r + 1][c].visited():
                breakable.add((r + 1, c))
        if c != 0:
            if self.mz[r][c - 1].visited():
                breakable.add((r, c - 1))
        if c != self.field_width - 1:
            if self.mz[r][c + 1].visited():
                breakable.add((r, c + 1))

        # Select a possible room at random
        r1, c1 = breakable.pop()
        # Break the walls separating the rooms
        if r1 == r:
            if c1 < c:
                # The wall of the front room
                self.mz[r][c].breakWall(maze_room.L_WALL)
                # The (same) wall of the visited room
                self.mz[r1][c1].breakWall(maze_room.R_WALL)
                # Update the representation
                self.disp.connectRooms(r, c, r1, c1)
            else:
                self.mz[r][c].breakWall(maze_room.R_WALL)
                self.mz[r1][c1].breakWall(maze_room.L_WALL)
                self.disp.connectRooms(r, c, r1, c1)
        else:
            if r1 < r:
                self.mz[r][c].breakWall(maze_room.U_WALL)
                self.mz[r1][c1].breakWall(maze_room.D_WALL)
                self.disp.connectRooms(r, c, r1, c1)
            else:
                self.mz[r][c].breakWall(maze_room.D_WALL)
                self.mz[r1][c1].breakWall(maze_room.U_WALL)
                self.disp.connectRooms(r, c, r1, c1)
        if self.DEBUG >= 1:
            print("Clear breakable: size = ", breakable.len())

    def drawGame(self):
        # Generate the maze
        
        # select the starting point and mark it visited
        col = random.randint(0, self.field_width - 1)
        row = random.randint(0, self.field_height - 1)
        self.mz[row][col].visit()
        #print("Starting point: ", (row, col))
        
        # Set up the front
        front = self.RoomSet()
        front = self.addToFront(front, (row, col))
        
        # Propagate - the algorithm is known as
        # "the modified randomized Prim's algorithm"
        while front.len() > 0: # While rooms in front
            # Select one as the next visited
            row, col = front.pop()
            self.mz[row][col].visit()
            # Add it to the maze
            self.breakWall(row, col)
            # Add the non-visited neighbours of the new maze room
            # to the front set
            front = self.addToFront(front, (row, col))
            if self.DEBUG >= 1:
                print("front size = ", front.len())
            
            if self.DEBUG > 1:
                messagebox.showinfo("Break", "continue")
        if self.DEBUG >= 1:
            print("Generated: count = ", count)
            input("press any key")
            
        # select entry location (lower side)
        row = self.field_height - 1
        col = random.randint(0, self.field_width - 1)
        # Don't break the logical wall - the walker shouldn't
        # wander outside the maze
        # self.mz[row][col].breakWall(maze_room.D_WALL)
        # Show the entry location nevertheless
        self.disp.breakWall(row, col, 'D')
        # And put the walker there
        self.walker = (row, col)
        self.disp.setWalker(row, col)
        
        # select exit location (upper side)
        row = 0
        col = random.randint(0, self.field_width - 1)
        # Allow moving out to finish the maze
        # The walker never exits, though
        self.mz[row][col].breakWall(maze_room.U_WALL)
        self.disp.breakWall(row, col, 'U')
        # messagebox.showinfo("Break", "continue")
        self.exit = (row, col)
        # Make the goal more visible
        self.disp.setGoal(row, col)
        
    def move(self, mv):
        # Move the walker
        r, c = self.walker # from where
        #print("room ",r,c," = ", hex(self.mz[r][c].getRoom()))
        # Try to move where the player ordered
        if mv == 'U': # upwards
            if self.mz[r][c].hasWall(maze_room.U_WALL):
                pass # Can't move - there's a logical wall
            else:
                x, y = self.exit # If we are in the front of exit
                if (x == r) and (y == c):
                    # Don't move, but announce the maze solved...
                    messagebox.showinfo("Ratkaistu", "Olet ratkaissut labyrintin")
                    return True # ... and leave the game
                # else, move as ordered
                self.walker = (r - 1, c)
                self.disp.moveWalker(r - 1, c)
        elif mv == 'D':
            if self.mz[r][c].hasWall(maze_room.D_WALL):
                pass
            else:
                self.walker = (r + 1, c)
                self.disp.moveWalker(r + 1, c)
        elif mv == 'L':
            if self.mz[r][c].hasWall(maze_room.L_WALL):
                pass
            else:
                self.walker = (r, c - 1)
                self.disp.moveWalker(r, c - 1)
        elif mv == 'R':
            if self.mz[r][c].hasWall(maze_room.R_WALL):
                pass
            else:
                self.walker = (r, c + 1)
                self.disp.moveWalker(r, c + 1)
        return False # The quest continues

