import tkinter as tk
from tkinter import messagebox
import random
import maze_room
import maze_graphics

class MazeGame(object):
    DEBUG = 0
    mz = []
    class RoomSet(object):
        
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
            self.coll.clear()

    def __init__(self, field, x, y):
        self.field_height = x
        self.field_width = y
        self.walker = (0,0)
        self.field = field
        # self.mz = [[0]*width for i in range(height)]
        for i in range(0, x):
            self.mz.append([])
            for j in range(0, y):
                rm = maze_room.MazeRoom()
                self.mz[i].append(rm)
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
        # Adds the neighbouring rooms to the front
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

        r1, c1 = breakable.pop()
        if r1 == r:
            if c1 < c:
                self.mz[r][c].breakWall(maze_room.L_WALL)
                self.mz[r1][c1].breakWall(maze_room.R_WALL)
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
        #breakable.clear()

    def drawGame(self):
        # Generate the maze
        
        # select the starting point
        col = random.randint(0, self.field_width - 1)
        row = random.randint(0, self.field_height - 1)
        self.mz[row][col].visit()
        print("Starting point: ", (row, col))
        # propagate
        front = self.RoomSet()
        front = self.addToFront(front, (row, col))
        count = 0
        while front.len() > 0:
            count += 1
            row, col = front.pop()
            self.mz[row][col].visit()
            self.breakWall(row, col)
            front = self.addToFront(front, (row, col))
            if self.DEBUG >= 1:
                print("front size = ", front.len())
            
            if self.DEBUG > 1:
                messagebox.showinfo("Break", "continue")
        if self.DEBUG >= 1:
            print("Generated: count = ", count)
            input("press any key")
        # select entry
        row = self.field_height - 1
        col = random.randint(0, self.field_width - 1)
        #self.mz[row][col].breakWall(maze_room.D_WALL)
        self.disp.breakWall(row, col, 'D')
        self.walker = (row, col)
        self.disp.setWalker(row, col)
        # select exit
        row = 0
        col = random.randint(0, self.field_width - 1)
        self.mz[row][col].breakWall(maze_room.U_WALL)
        self.disp.breakWall(row, col, 'U')
        # messagebox.showinfo("Break", "continue")
        self.exit = (row, col)
        self.disp.setGoal(row, col)
        
    def move(self, mv):
        # Move the walker
        r, c = self.walker
        #print("room ",r,c," = ", hex(self.mz[r][c].getRoom()))
        if mv == 'U':
            if self.mz[r][c].hasWall(maze_room.U_WALL):
                pass
            else:
                x, y = self.exit
                if (x == r) and (y == c):
                    messagebox.showinfo("Ratkaistu", "Olet ratkaissut labyrintin")
                    return True
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
        return False

