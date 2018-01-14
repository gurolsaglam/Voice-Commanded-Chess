import Piece

class Tile:
	__Owner = None
	__x = 0
	__y = 0

	def __init__(self,tx,ty):
		self.__x = tx
		self.__y = ty

	def isEmpty(self):
		if self.__Owner == None:
			return True
		return False

	def setOwner(self,Owner):
		self.__Owner = Owner
		self.__Owner.setTile(self)

	def removeOwner(self):
		self.__Owner = None
		if(self.__Owner == self):
			self.__Owner.setTile(None)
		
	def getOwner(self):
		return self.__Owner

	def getX(self):
		return self.__x
	
	def getY(self):
		return self.__y
	
	def isPathLShaped(self,targetTile):
		return ((abs(targetTile.getX() - self.__x) == 1 and abs(targetTile.getY() -self.__y) == 2) or
		((abs(targetTile.getX() - self.__x) == 2) and abs(targetTile.getY() - self.__y) == 1))

	def isPathVertical(self,targetTile):
		return (targetTile.getX() == self.__x)

	def isPathHorizontal(self,targetTile):
		return (targetTile.getY() == self.__y)

	def isPathDiagonal(self,targetTile):
		return (abs(targetTile.getX() - self.__x) == abs(targetTile.getY() - self.__y))

	def getVerticalDistance(self,targetTile):
		if(self.isPathVertical(targetTile)): return abs(targetTile.getY() - self.__y)
		return -1

	def getHorizontalDistance(self,targetTile):
		if(self.isPathHorizontal(targetTile)): return abs(targetTile.getX() - self.__x)
		return -1

	def getDiagonalDistance(self,targetTile):
		if(self.isPathDiagonal(targetTile)): return abs(targetTile.getX() - self.__x)
		return -1