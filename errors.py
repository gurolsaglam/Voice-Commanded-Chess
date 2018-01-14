class IllegalMovement(Exception):
	def __init__(self):
		pass
	
	def __str__(self):
		return "This is not a legal movement."

class NotPlayersPiece(Exception):
	def __init__(self):
		pass
	
	def __str__(self):
		return "This is not your piece."

class EmptyHeadTile(Exception):
	def __init__(self):
		pass
	
	def __str__(self):
		return "This is an empty tile."





class NotApplicablePromotion(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return "You are trying to promote to " + self.value + ", but this piece is not captured yet."

class NotAPawn(Exception):
	def __init__(self, value):
		self.value = value
	
	def __str__(self):
		return "You are trying to promote a piece that is not a pawn."
