from tkinter import Tk
from Board import Board
from SpeechSideFrame import SpeechSideFrame


root = Tk(screenName = "CHESS", baseName = "CHESS")

board = Board(root = root, height = 600, width = 600)

sideFrame = SpeechSideFrame(parent = root, board = board)

root.mainloop()