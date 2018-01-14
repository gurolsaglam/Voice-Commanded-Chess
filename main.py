from tkinter import Tk
from Board import Board
from SideFrame import SideFrame


root = Tk(screenName = "CHESS", baseName = "CHESS")

board = Board(root = root, height = 600, width = 600)

sideFrame = SideFrame(parent = root, board = board)

#root.update()
root.mainloop()