#!/usr/bin/python3
# Maze main program

import tkinter as tk
import maze_room
import maze_game
import maze_graphics

# about full screen on my development laptop
x = 50 # height in rooms
y = 90 # width in rooms

class Application(tk.Frame):
    # The application class
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.x = x
        self.y = y
        self.grid()
        self.field = self.createWidgets(x, y)
        self.game = maze_game.MazeGame(self.field, self.x - 2, self.y - 2)
        self.playGame()
        
    def createWidgets(self, x, y):
        yy = y * maze_graphics.ROOM_WIDTH_IN_PIX
        xx = x * maze_graphics.ROOM_HEIGHT_IN_PIX
        field = tk.Canvas(self, width=yy, height=xx, background=maze_graphics.BGC)
        field.grid()
        # print("Canvas: xx=", xx, " yy=", yy, " w=", field.winfo_reqwidth(), " h=", field.winfo_reqheight())
        # self.quitButton = tk.Button(self, text='Quit', command=self.stopGame)
        # self.quitButton.grid()
        # self.quitButton = tk.Button(self, text='Start', command=self.playGame)
        # self.quitButton.grid()
        self.textLabel = tk.Label(self, text="Use arrow keys, 'q' = quit")
        self.textLabel.grid()
        return field

    def addHandler(self, field):
        # Adds a key handler
        seq = '<Any-KeyPress>'
        field.bind_all(sequence=seq, func=self.handleKey, add=None)
        
    def initGame(self):
        # Sets up the maze itself
        self.game.clearGame()
        self.game.drawGame()

    def stopGame(self):
        # Kills the application
        self.done = True
        self.quit()

    def handleKey(self, event):
        # Handler for key presses
        if False:
            print("handleKey: ", event.keysym, event.keycode, event.keysym_num)
        mv = None
        if event.keycode == 104: # Down
            mv = 'D'
        elif event.keycode == 100: # Left
            mv = 'L'
        elif event.keycode == 102: # Right
            mv = 'R'
        elif event.keycode == 98: # Up
            mv = 'U'
        elif event.keycode == 88: # KP_Down
            mv = 'D'
        elif event.keycode == 80: # KP_Up
            mv = 'U'
        elif event.keycode == 83: # KP_Left
            mv = 'L'
        elif event.keycode == 85: # KP_Right
            mv = 'R'
        elif event.keysym == 'Down': # ??_Down
            mv = 'D'
        elif event.keysym == 'Up': # ??_Up
            mv = 'U'
        elif event.keysym == 'Left': # ??_Left
            mv = 'L'
        elif event.keysym == 'Right': # ??_Right
            mv = 'R'
        elif event.keycode == 24: # 'Q' or 'q'
            self.stopGame()
            return
        else:
            return
        # Player's move
        if self.game.move(mv):
            # Solved - exit the program
            self.stopGame()
            
    def playGame(self):
        # Starts the game
        self.initGame()
        self.addHandler(self.field)
        # return in App mainloop to play
        
#print("Sokkelo")
#y = int(input("Anna leveys: "))
#x = int(input("Anna korkeus: "))
root = tk.Tk() # root.destroy() needs this
app = Application()
app.master.title('Sokkelo - Maze')
app.mainloop()
#print("Game over")
root.destroy() # some IDEs need this
