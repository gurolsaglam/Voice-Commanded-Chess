from tkinter import PhotoImage

BimagePath = [ None, "./blackpieces/bpawn.png", "./blackpieces/bknight.png", "./blackpieces/bbishop.png",
				"./blackpieces/brook.png", "./blackpieces/bqueen.png", "./blackpieces/bking.png"]
WimagePath = [None, "./whitepieces/wpawn.png", "./whitepieces/wknight.png", "./whitepieces/wbishop.png",
				"./whitepieces/wrook.png", "./whitepieces/wqueen.png", "./whitepieces/wking.png"]

class Piece:
	__type = 0
	__tile = None
	__isWhite = False
	__isMovedBefore = False
	def __init__(self,typeInput,isWhite): ### empty 0 - p 1 - n 2 - b 3 - r 4 - q 5 - k 6
		self.__type = typeInput
		self.__isWhite = isWhite

	def isLegalMovement(self, headTile,targetTile):
		pass

	def isLegalCapturing(self,headTile,targetTile):
		pass

	def move(self,headTile,targetTile):
		if (self.isLegalMovement(headTile, targetTile) or self.isLegalCapturing(headTile, targetTile)):
			targetTile.setOwner(self)
			headTile.removeOwner()
			self.__isMovedBefore = True
			return True
		return False

	def imagineMove(self,headTile,targetTile):
		if(self.isLegalMovement(headTile,targetTile) or self.isLegalCapturing(headTile,targetTile)):
			targetTile.setOwner(self)
			headTile.removeOwner()
			return True
		return False

	def promote(self,typePromote):
		if(self.__type == 1):
			self.__type = typePromote
			if(typePromote == 2):
				self.__class__ = Knight
				return True
			elif(typePromote == 3):
				self.__class__ = Bishop
				return True
			elif(typePromote == 4):
				self.__class__ = Rook
				return True
			elif(typePromote == 5):
				self.__class__ = Queen
				return True
		return False
	
	def setTile(self,tile):
		self.__tile = tile

	def getTile(self):
		return self.__tile
	
	def getType(self):
		return self.__type
	
	def getIsWhite(self):
		return self.__isWhite
	
	def getIsMovedBefore(self):
		return self.__isMovedBefore
	
	def getImage(self, master):
		if (self.__isWhite):
			self.image = PhotoImage(master = master, file = WimagePath[self.__type])
			return self.image
		else:
			self.image = PhotoImage(master = master, file = BimagePath[self.__type])
			return self.image


class Pawn(Piece):

	def __init__(self,isWhite):
		Piece.__init__(self, 1,isWhite)

	def isLegalMovement(self, headTile,targetTile):

		if(not self.getIsMovedBefore()): ## first strike rule
			return  (headTile.isPathVertical(targetTile)
				and headTile.getVerticalDistance(targetTile) <= 2 and targetTile.getOwner() == None)
		
		return (headTile.isPathVertical(targetTile)
				and headTile.getVerticalDistance(targetTile) == 1 and targetTile.getOwner() == None)


	def isLegalCapturing(self,headTile,targetTile):##add el passant rule
		return (headTile.isPathDiagonal(targetTile)
				and headTile.getDiagonalDistance(targetTile) == 1 and not (targetTile.getOwner().getIsWhite() == self.getIsWhite()))


class Knight(Piece):
	def __init__(self,isWhite):
		Piece.__init__(self, 2,isWhite)
	def isLegalMovement(self, headTile,targetTile):
		return (headTile.isPathLShaped(targetTile) and targetTile.getOwner() == None)
	def isLegalCapturing(self,headTile,targetTile):
		return (headTile.isPathLShaped(targetTile) and not (targetTile.getOwner().getIsWhite() == self.getIsWhite()))

class Bishop(Piece):
	def __init__(self,isWhite):
		Piece.__init__(self, 3,isWhite)
	def isLegalMovement(self, headTile,targetTile):
		return (headTile.isPathDiagonal(targetTile) and targetTile.getOwner() == None)
	def isLegalCapturing(self, headTile, targetTile):
		return headTile.isPathDiagonal(targetTile) and not (targetTile.getOwner().getIsWhite() == self.getIsWhite())


class Rook(Piece):
	def __init__(self,isWhite):
		Piece.__init__(self, 4,isWhite)
	def isLegalMovement(self, headTile,targetTile):
		return ((headTile.isPathVertical(targetTile)
				or headTile.isPathHorizontal(targetTile)) and targetTile.getOwner() == None)
	def isLegalCapturing(self,headTile,targetTile):
		return ((headTile.isPathVertical(targetTile)
				or headTile.isPathVertical) and not (targetTile.getOwner().getIsWhite() == self.getIsWhite()))


class Queen(Piece):
	def __init__(self,isWhite):
		Piece.__init__(self, 5,isWhite)

	def isLegalMovement(self, headTile,targetTile):
		return ((headTile.isPathVertical(targetTile)
				or headTile.isPathHorizontal(targetTile)
				or headTile.isPathDiagonal(targetTile)) and targetTile.getOwner() == None)
	def isLegalCapturing(self,headTile,targetTile):
		return ((headTile.isPathVertical(targetTile)
				or headTile.isPathHorizontal(targetTile)
				or headTile.isPathDiagonal(targetTile)) and not (targetTile.getOwner().getIsWhite() == self.getIsWhite()))

class King(Piece):
	def __init__(self,isWhite):
		Piece.__init__(self, 6,isWhite)
	def isLegalMovement(self, headTile, targetTile):
		if (targetTile.getOwner() == None):
			if ( headTile.isPathVertical( targetTile ) ):
				return (headTile.getVerticalDistance(targetTile) == 1)

			if ( headTile.isPathHorizontal(targetTile) ):
				return (headTile.getHorizontalDistance(targetTile) == 1)

			if ( headTile.isPathDiagonal( targetTile ) ):
				return (headTile.getDiagonalDistance(targetTile) == 1)
		return False
	
	def isLegalCapturing(self, headTile, targetTile):
		if not (targetTile.getOwner().getIsWhite() == self.getIsWhite()):
			if ( headTile.isPathVertical( targetTile ) ):
				return (headTile.getVerticalDistance(targetTile) == 1)

			if ( headTile.isPathHorizontal(targetTile) ):
				return (headTile.getHorizontalDistance(targetTile) == 1)

			if ( headTile.isPathDiagonal( targetTile ) ):
				return (headTile.getDiagonalDistance(targetTile) == 1)
		return False