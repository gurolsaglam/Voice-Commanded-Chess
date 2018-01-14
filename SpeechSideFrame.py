from tkinter import Frame, Tk, Label, Button, RIDGE, Text, INSERT, END, WORD, DISABLED, NORMAL, Scrollbar, RIGHT, Y
from Board import Board
from SpeechRecognizer import SpeechRecognizer
from errors import *

class SpeechSideFrame:
	
	def __init__(self, parent = None, width = 225, height = 630, board = None):
		self.__parent = parent
		self.__width = width
		self.__height = height
		
		if (not parent == None):
			self.__frame = Frame(parent, width = width, height = height)
		elif (board == None):
			self.__parent = Tk()
			self.__frame = Frame(self.__parent, width = width, height = height)
		else:
			self.__parent = board.getRoot()
			self.__frame = Frame(self.__parent, width = width, height = height)
		
		self.__frame.grid(row = 0, column = 1)
		
		if (board == None):
			self.__board = Board(self.__parent)
		else:
			self.__board = board
		
		self.__initCommandText(x = 0, y = 0, height = height/2, width = width)
		lblheight = int(height/8)
		self.__initPlayerLabel(x = (width - lblheight)/2, y = height/14 + height/2, height = lblheight, width = lblheight)
		btnheight = int(height/6)
		self.__initPlayButton(x = (width - btnheight)/2, y = height/7 + lblheight + height/2, height = btnheight, width = btnheight)
		
	
	def __initCommandText(self, x, y, height, width):
		self.__commandText = Text(self.__frame, fg = "whitesmoke", bg = "gray12", font = ('Helvetica', 7), borderwidth = 1, wrap = WORD)
		self.__commandText.place(x = x, y = y, height = height, width = width)
		self.__commandText.insert(INSERT, "Frame Initialized.")
		self.__commandText.config(state = DISABLED)
		
		scrollbar = Scrollbar(self.__commandText)
		scrollbar.pack(side = RIGHT, fill = Y)
		self.__commandText.config(yscrollcommand = scrollbar.set)
		scrollbar.config(command = self.__commandText.yview)
	
	def __initPlayerLabel(self, x, y, height, width):
		self.__playerLabel = Label(self.__frame, text = "Turn: White.", fg = "dimgrey", bg = "whitesmoke", borderwidth = 1, relief = RIDGE)
		self.__playerLabel.place(x = x, y = y, height = height, width = width)
	
	def __initPlayButton(self, x, y, height, width, text = "Play", command = None):
		if (command == None):
			self.__playButton = Button(self.__frame, text = str(text), command = self.__isPushed)
			self.__playButton.place(x = x, y = y, height = height, width = width)
		else:
			self.__playButton = Button(self.__frame, text = str(text), command = command)
			self.__playButton.place(x = x, y = y, height = height, width = width)
	
	def __isPushed(self):
		srListener = SpeechRecognizer(commandText = self.__commandText)
		
		while True:
			speech = srListener.audio2text_google()
			if (speech == 0):
				print("Could not request results, it is about api do not worry")
				self.__printToCommandText("Could not request results, it is about api do not worry")
			elif (speech == -2):
				print("Sorry, i could not understand you")
				self.__printToCommandText("Sorry, i could not understand you")
			else:
				print("Recognized sentence: ", speech)
				self.__printToCommandText("Recognized sentence: " + speech)
				speech = str(speech)
				if(len(speech) == 4):
					yOld = int(speech[1]) - 1
					xOld = int(104-ord(speech[0]))
					yNew = int(speech[3]) - 1
					xNew = int(104-ord(speech[2]))
				
					try:
						isMoved = self.__board.movePiece(xOld,yOld,xNew,yNew)
						if (isMoved):
							move = "xOld = " + str(xOld) + " yOld " + str(yOld) + " xNew " + str(xNew) + " yNew " + str(yNew)
							print(move)
							self.__printToCommandText(move)
							if (self.__playerLabel.cget("bg") == "whitesmoke"):
								self.__playerLabel.config(bg = "dimgrey", fg = "whitesmoke", text = "Turn: Black.")
							else:
								self.__playerLabel.config(bg = "whitesmoke", fg = "dimgrey", text = "Turn: White.")
							break
					except IllegalMovement as e:
						print("not moved.")
						self.__printToCommandText("not moved.")
						print(e)
						self.__printToCommandText(e)
					except NotPlayersPiece as e:
						print("not moved.")
						self.__printToCommandText("not moved.")
						print(e)
						self.__printToCommandText(e)
					except EmptyHeadTile as e:
						print("not moved.")
						self.__printToCommandText("not moved.")
						print(e)
						self.__printToCommandText(e)
				elif (len(speech) == 3):
					y = int(speech[1]) -1
					x = int(104-ord(speech[0]))
					typePromote = int(speech[2])
					
					try:
						isMoved = False
						isMoved = self.__board.promotePawnAt(x = x, y = y, typePromote = typePromote)
						if (isMoved):
							move = "x = " + str(x) + " y " + str(y) + "	type " + str(typePromote)
							print(move)
							self.__printToCommandText(move)
							if (self.__playerLabel.cget("bg") == "whitesmoke"):
								self.__playerLabel.config(bg = "dimgrey", fg = "whitesmoke", text = "Turn: Black.")
							else:
								self.__playerLabel.config(bg = "whitesmoke", fg = "dimgrey", text = "Turn: White.")
							break
					except NotPlayersPiece as e:
						print("not moved.")
						self.__printToCommandText("not moved.")
						print(e)
						self.__printToCommandText(e)
					except EmptyHeadTile as e:
						print("not moved.")
						self.__printToCommandText("not moved.")
						print(e)
						self.__printToCommandText(e)
				elif (speech == "-1"):
					self.__parent.quit()
					exit()
	
	def __printToCommandText(self, string):
		self.__commandText.config(state = NORMAL)
		self.__commandText.insert(END, "\n" + str(string))
		self.__commandText.config(state = DISABLED)
	
	def _setBoard(self,board):
		self.__board = board
	
	def __del__(self):
		del self.__width
		del self.__height
		del self.__commandText
		del self.__playerLabel
		del self.__playButton
		del self.__frame