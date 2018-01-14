from tkinter import Canvas, Tk, PhotoImage
from Tile import Tile
from Piece import *
from errors import *

numOfRows = 8
numOfColumns = 8
sideLength = 30

class Board:
	
	__isWhitesTurn = True
	__whiteKing = None
	__blackKing = None
	
	#this method initializes the pieces without the GUI components.
	def __initPieces(self):
		self.__tiles = [0] * 8
		for i in range(0, len(self.__tiles)):
			self.__tiles[i] = [0] * 8
			for j in range(0, len(self.__tiles[i])):
				self.__tiles[i][j] = Tile(tx = i, ty = j)
		(self.__tiles[0][0]).setOwner(Rook(True))
		(self.__tiles[1][0]).setOwner(Knight(True))
		(self.__tiles[2][0]).setOwner(Bishop(True))
		self.__whiteKing = King(True)
		(self.__tiles[3][0]).setOwner(self.__whiteKing)
		(self.__tiles[4][0]).setOwner(Queen(True))
		(self.__tiles[5][0]).setOwner(Bishop(True))
		(self.__tiles[6][0]).setOwner(Knight(True))
		(self.__tiles[7][0]).setOwner(Rook(True))
		for i in range(0,8):
			(self.__tiles[i][1]).setOwner(Pawn(True))
		for i in range(0,8):
			(self.__tiles[i][6]).setOwner(Pawn(False))
		(self.__tiles[0][7]).setOwner(Rook(False))
		(self.__tiles[1][7]).setOwner(Knight(False))
		(self.__tiles[2][7]).setOwner(Bishop(False))
		self.__blackKing = King(False)
		(self.__tiles[3][7]).setOwner(self.__blackKing)
		(self.__tiles[4][7]).setOwner(Queen(False))
		(self.__tiles[5][7]).setOwner(Bishop(False))
		(self.__tiles[6][7]).setOwner(Knight(False))
		(self.__tiles[7][7]).setOwner(Rook(False))
	
	#this method adds the images of the pieces to the GUI board. Not to be used if the Board GUI is not initialized.
	def __addPiecestoBoard(self):
		self.__images = {}
		for i in range(0, numOfRows):
			for j in range(0, numOfColumns):
				box = i, j
				if (not (self.__tiles[i][j]).getOwner() == None):
					image = ((self.__tiles[i][j]).getOwner()).getImage(master = self.__canvas)
					image = (image).subsample(self.__scale_h)
					(self.__canvas).create_image((self.__height/numOfRows)*i + 40 + sideLength, (self.__width/numOfColumns)*j + 35 + sideLength, image = image, tags= str(i)+str(j))
					self.__images[(i, j)] = box, image
				else:
					self.__images[(i, j)] = box, None
		self.__canvas.update
	
	#this method initializes the Board GUI and calls the __addPiecestoBoard function.
	def __initBoardView(self):
		for i in range(0, numOfRows):
			self.__canvas.create_rectangle(0, i * (self.__height/numOfRows) + sideLength, 
					sideLength, (i+1) * (self.__height/numOfRows) + sideLength, fill = "lightgrey")
			self.__canvas.create_text(sideLength/2, (i+0.5)*(self.__height/numOfRows) + sideLength, text = str(i+1), font = ('Helvetica', 20, 'bold'), justify = 'center', fill = 'black', tags = "num" + str(i + 1))
		for j in range(0, numOfRows):
			self.__canvas.create_rectangle(j * (self.__width/numOfColumns) + sideLength, 0, 
					(j+1) * (self.__width/numOfColumns) + sideLength, sideLength, fill = "lightgrey")
			self.__canvas.create_text((j+0.5) * (self.__width/numOfColumns) + sideLength, sideLength/2, text = str(chr((numOfRows - 1 - j) + 65)), font = ('Helvetica', 20, 'bold'), justify = 'center', fill = 'black', tags = "alph" + str(i + 1))
		
		for i in range(0, numOfRows):
			for j in range(0, numOfColumns):
				if((i + j)%2 == 0):
					self.__canvas.create_rectangle(j * (self.__width/numOfColumns) + sideLength, i * (self.__height/numOfRows) + sideLength, 
						(j+1) * (self.__width/numOfColumns) + sideLength, (i+1) * (self.__height/numOfRows) + sideLength, fill = "whitesmoke")
				else:
					self.__canvas.create_rectangle(j * (self.__width/numOfColumns) + sideLength, i * (self.__height/numOfRows) + sideLength,
						(j+1) * (self.__width/numOfColumns) + sideLength, (i+1) * (self.__height/numOfRows) + sideLength, fill = "dimgrey")
		
		self.__addPiecestoBoard()
		self.__canvas.update
	
	#The constructor for the Board object.
	def __init__(self, root = None, width = 600, height = 600):
		self.__root = root
		self.__width = width
		self.__height = height
		self.__isWhitesTurn = True
		self.__canvas = 0
		if (not root == None):
			self.__canvas = Canvas(root, width = width + sideLength, height = height + sideLength)
		else:
			self.__root = Tk()
			self.__canvas = Canvas(self.__root, width = width + sideLength, height = height + sideLength)
		self.__canvas.grid(row = 0, column = 0)# pack(expand = True)
		
		self.__scale_h = 320/(self.__height/numOfColumns)
		self.__scale_h = int(((self.__scale_h * 10)-((self.__scale_h * 10)%10))/10)
		
		self.__initPieces()
		self.__initBoardView()
		#ILLEGAL MOVE
		#self.movePiece(2,6,2,2)
		#LEGAL MOVE
		#self.movePiece(2,6,2,5)
	
	#Clearer implementation to move a piece.
	def movePiece(self, xOld, yOld, xNew, yNew):
		if (not self.__tiles[xOld][yOld].getOwner() == None):
			if (self.__isWhitesTurn == self.__tiles[xOld][yOld].getOwner().getIsWhite()):
				if (self.isLegalMove(self.__tiles[xOld][yOld],self.__tiles[xNew][yNew])):
					if(not self.isCheckPrevented(xOld,yOld,xNew,yNew)):
						return False
					self.__tiles[xOld][yOld].getOwner().move(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew])
					self.__isWhitesTurn = not self.__isWhitesTurn
					image = ((self.__tiles[xNew][yNew]).getOwner()).getImage(master=self.__canvas)
					image = (image).subsample(self.__scale_h)
					self.__images[(xOld, yOld)] = self.__images[(xOld, yOld)][0], None
					self.__images[(xNew, yNew)] = (xNew, yNew), image
					self.__canvas.create_image((self.__height / numOfRows) * xNew + 40 + sideLength,
											   (self.__width / numOfColumns) * yNew + 35 + sideLength, image=image,
											   tags=str(xNew) + str(yNew))
					self.__canvas.update
					return True
				elif (not self.__tiles[xNew][yNew].getOwner() == None):
					if (self.isLegalCapture(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew]) ):
						if(not self.isCheckPrevented(xOld,yOld,xNew,yNew)):
							return False
						self.__tiles[xOld][yOld].getOwner().move(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew])
						self.__isWhitesTurn = not self.__isWhitesTurn
						image = ((self.__tiles[xNew][yNew]).getOwner()).getImage(master=self.__canvas)
						image = (image).subsample(self.__scale_h)
						self.__images[(xOld, yOld)] = self.__images[(xOld, yOld)][0], None
						self.__images[(xNew, yNew)] = (xNew, yNew), image
						self.__canvas.create_image((self.__height / numOfRows) * xNew + 40 + sideLength,
												   (self.__width / numOfColumns) * yNew + 35 + sideLength, image=image,
												   tags=str(xNew) + str(yNew))
						self.__canvas.update
						return True
					else:
						return False
				else:
					# print("This is not a legal movement.")
					raise IllegalMovement()
			else:
				# print("This is not this player's piece.")
				raise NotPlayersPiece()
		else:
			# print("No piece exists in that tile.")
			raise EmptyHeadTile()
	
	def scanPieces(self,isWhite):
		tmpList = []
		if(isWhite):
			self.__whitePieces = []
			tmpList = self.__whitePieces
		else:
			self.__blackPieces = []
			tmpList = self.__blackPieces

		for i in self.__tiles:
			for j in i:
				if(j.getOwner().getIsWhite == isWhite):
					tmpList.append(j)
	
	def promotePawnAt(self, x, y, typePromote):
		if (not self.__tiles[x][y].getOwner() == None):
			if (self.__tiles[x][y].getOwner().getIsWhite() == self.__isWhitesTurn):
				if (self.__tiles[x][y].getOwner().promote(typePromote)):
					self.__isWhitesTurn = not self.__isWhitesTurn
					
					image = ((self.__tiles[x][y]).getOwner()).getImage(master = self.__canvas)
					image = (image).subsample(self.__scale_h)
					self.__images[(x, y)] = (x, y), image
					self.__canvas.create_image((self.__height/numOfRows) * x + 40 + sideLength, (self.__width/numOfColumns) * y + 35 + sideLength, image = image, tags = str(x) + str(y))
					self.__canvas.update
					return True
			else:
				# print("This is not your piece.")
				raise NotPlayersPiece()
		else:
			# print("You do not have a piece in that tile.")
			raise EmptyHeadTile()
	
	def getRoot(self):
		return self.__root
	
	def CastleRule(self,isWhite):
		if(isWhite):
			#kingside castle
			if (not self.__whiteKing.getIsMovedBefore() and self.getFirstPiece(self.__tiles[3][0],-1,0).getType() == 4
														and not self.__tiles[0][0].getIsMovedBefore()):
				for i in range(1,3):
					if( self.VHEnemyControl(i,0) and self.diagonalEnemyControl(i,0)):
						return False
				return True
			else:
				pass

			#queenside castle
	
	def isCheckPrevented(self,xOld,yOld,xNew,yNew):
		if(self.isCheck(True) and self.__isWhitesTurn and not self.isCheck(False)):
			self.__tiles[xOld][yOld].getOwner().imagineMove(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew])
			print("White has to prevent Check")
			if (self.isCheck(True) and self.__isWhitesTurn and not self.isCheck(False)):
				self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
				return False
			self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
		elif(self.isCheck(False) and not self.__isWhitesTurn and not self.isCheck(True)):
			print("Black has to prevent Check")
			self.__tiles[xOld][yOld].getOwner().imagineMove(self.__tiles[xOld][yOld],self.__tiles[xOld][yOld])
			if(self.isCheck(False) and not self.__isWhitesTurn and not self.isCheck(True)):
				self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
				return False
			self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
		elif(self.isCheck(True) and self.isCheck(False)):
			print("Both are check , turn owner won")
		elif(not self.isCheck(True) and self.__isWhitesTurn):
			self.__tiles[xOld][yOld].getOwner().imagineMove(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew])
			if(self.isCheck(True)):
				self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
				return False
			self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
		elif(not self.isCheck(False) and not self.__isWhitesTurn):
			self.__tiles[xOld][yOld].getOwner().imagineMove(self.__tiles[xOld][yOld], self.__tiles[xNew][yNew])
			if (self.isCheck(False)):
				self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
				return False
			self.__tiles[xNew][yNew].getOwner().imagineMove(self.__tiles[xNew][yNew], self.__tiles[xOld][yOld])
		return True
	
	def isVerticalPathEmpty(self, headTile, targetTile):
		if (targetTile.getX() == headTile.getX()):
			start = headTile.getY()
			end = targetTile.getY()
			if (start > end):
				temp = end
				end = start
				start = temp
			start = start + 1
			for i in range(start, end):
				if not ((self.__tiles[headTile.getX()][i]).getOwner() == None): 
					return False
			return True
		return False

	def isHorizontalPathEmpty(self, headTile, targetTile):
		if (targetTile.getY() == headTile.getY()):
			start = headTile.getX()
			end = targetTile.getX()
			if (start > end):
				temp = end
				end = start
				start = temp
			start = start + 1
			for i in range(start, end):
				if not ((self.__tiles[i][headTile.getY()]).getOwner() == None): 
					return False
			return True
		return False

	def isDiagonalPathEmpty(self, headTile, targetTile):
		dx = targetTile.getX() - headTile.getX()
		dy = targetTile.getY() - headTile.getY()
		if (dx == dy or dx == -1 * dy):
			xVector = int(dx / abs(dx))
			yVector = int(dy / abs(dy))
			for i in range(1, abs(dx)):
				if not ((self.__tiles[headTile.getX() + xVector * i][ headTile.getY() + yVector * i]).getOwner() == None):
					return False
			return True
		return False

	def diagonalEnemyControl(self, headTile, isHeadWhite):
		x = headTile.getX()
		y = headTile.getY()
		tmpPiece = None
		for dx in range(-1, 2, 2):
			for dy in range(-1, 2, 2):
				tmpPiece = self.getFirstPiece(headTile, dx, dy)
				if not tmpPiece == None:
					if (tmpPiece.getIsWhite() != isHeadWhite and (tmpPiece.getType() == 3 
							or tmpPiece.getType() == 5 or (tmpPiece.getType() == 1 
							and headTile.getDiagonalDistance(tmpPiece.getTile()) == 1))):
						return True
		return False

	def VHEnemyControl(self, headTile, isHeadWhite):
		tmpPiece = None
		for i in range(-1, 2, 2):
			tmpPiece = self.getFirstPiece(headTile, 0, i)
			if not tmpPiece == None:
				if (tmpPiece.getIsWhite() != isHeadWhite and 
						(tmpPiece.getType() == 4 or tmpPiece.getType() == 5)):
					return True
			tmpPiece = self.getFirstPiece(headTile, i, 0)
			if not tmpPiece == None:
				if ((tmpPiece.getType() == 4 and tmpPiece.getIsWhite() != isHeadWhite) or
						(tmpPiece.getType() == 5 and tmpPiece.getIsWhite() != isHeadWhite)):
					return True
		return False

	def getFirstPiece(self, headTile, xVector, yVector):
		x = headTile.getX()
		y = headTile.getY()
		for i in range(1, 8):
			if(x + xVector * i > 7 or y + yVector * i > 7 or x + xVector * i < 0 or y + yVector * i < 0):
				return None
			if ((self.__tiles[x + xVector * i][y + yVector * i]).getOwner() != None):
				return (self.__tiles[x + xVector * i][y + yVector * i]).getOwner()
		return None

	def knightEnemyControl(self, headTile, isHeadWhite):
		x = headTile.getX()
		y = headTile.getY()
		tmpPiece = None
		for dx in range (-2, 3, 1):
			for dy in range ( -2, 3, 1):
				if (dx != 0 and dy != 0 and dx != dy):
					if (x + dx >= 0 and x + dx <= 7 and y + dy >= 0 and y + dy <= 7):
						tmpPiece = self.__tiles[x + dx][y + dy].getOwner()
						if not tmpPiece == None:
							if tmpPiece.getType() == 2 and tmpPiece.getIsWhite() != isHeadWhite:
								return True
		return False
	
	def isReverseMove(self, headTile, targetTile):
		if (headTile.getOwner().getIsWhite()):
			return (((targetTile.getX() - headTile.getX()) >= 0) and ((targetTile.getY() - headTile.getY()) >= 0))
		return (((headTile.getX() - targetTile.getX()) >= 0) and ((headTile.getY() - targetTile.getY()) >= 0))
	
	def isLegalMove(self, headTile, targetTile):
		if (not targetTile.isEmpty()):
			return False
		piece = headTile.getOwner()
		if piece.getType() == 1:
			return (piece.isLegalMovement(headTile, targetTile)
				and (self.isVerticalPathEmpty(headTile, targetTile))
				and self.isReverseMove(headTile, targetTile))
		elif piece.getType() == 2:
			return (piece.isLegalMovement(headTile, targetTile))
		elif piece.getType() == 3:
			return (piece.isLegalMovement(headTile, targetTile) and self.isDiagonalPathEmpty(headTile, targetTile))
		elif piece.getType() == 4:
			if(piece.isLegalMovement(headTile, targetTile)):
				if (headTile.isPathVertical(targetTile)):
					return self.isVerticalPathEmpty(headTile, targetTile)
				if (headTile.isPathHorizontal(targetTile)):
					return self.isHorizontalPathEmpty(headTile, targetTile)
		elif piece.getType() == 5:
			if (piece.isLegalMovement(headTile, targetTile)):
				if (headTile.isPathVertical(targetTile)):
					return self.isVerticalPathEmpty(headTile, targetTile)
				if (headTile.isPathHorizontal(targetTile)):
					return self.isHorizontalPathEmpty(headTile, targetTile)
				if (headTile.isPathDiagonal(targetTile)):
					return self.isDiagonalPathEmpty(headTile, targetTile)
		elif piece.getType() == 6:
			return piece.isLegalMovement(headTile, targetTile)

	def isCheck(self,isHeadWhite):
		if(isHeadWhite):
			tile = self.__whiteKing.getTile()
			return self.VHEnemyControl(tile,True) or self.diagonalEnemyControl(tile,True) or self.knightEnemyControl(tile,True)
		else:
			tile = self.__blackKing.getTile()
			return self.VHEnemyControl(tile,False) or self.diagonalEnemyControl(tile,False) or self.knightEnemyControl(tile,False)
		return False

	def isStaleMate(self):
		pass

	def isWinCondition(self,isHeadWhite):
		tmpPiece = None
		if(isHeadWhite):
			tmpPiece = self.__whiteKing
		else:
			tmpPiece = self.__blackKing

		if(self.isCheck(isHeadWhite)):
			pass


		return False
	
	def isLegalCapture(self, headTile, targetTile):
		piece = headTile.getOwner()
		if piece.getType() == 1:
			return (piece.isLegalCapturing(headTile, targetTile)
				and self.isReverseMove(headTile, targetTile))
		elif piece.getType() == 2:
			return (piece.isLegalCapturing(headTile, targetTile))
		elif piece.getType() == 3:
			return (piece.isLegalCapturing(headTile, targetTile) and self.isDiagonalPathEmpty(headTile, targetTile))
		elif piece.getType() == 4:
			if(piece.isLegalCapturing(headTile, targetTile)):
				if(headTile.isPathVertical(targetTile)):
					return self.isVerticalPathEmpty(headTile, targetTile)
				if(headTile.isPathHorizontal(targetTile)):
					return self.isHorizontalPathEmpty(headTile, targetTile)
		elif piece.getType() == 5:
			if(piece.isLegalCapturing(headTile, targetTile)):
				if(headTile.isPathVertical(targetTile)):
					return self.isVerticalPathEmpty(headTile, targetTile)
				if(headTile.isPathHorizontal(targetTile)):
					return self.isHorizontalPathEmpty(headTile, targetTile)
				if(headTile.isPathDiagonal(targetTile)):
					return self.isDiagonalPathEmpty(headTile, targetTile)
		elif piece.getType() == 6:
			return piece.isLegalCapturing(headTile, targetTile)
	
	def __del__(self):
		del self.__width
		del self.__height
		del self.__canvas
		del self.__isWhitesTurn
		del self.__tiles
		del self.__images
