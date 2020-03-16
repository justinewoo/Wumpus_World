# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your self class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================
"""
Better version
Store ps instead of moves
While frontier is not empty
	Move to adjacent unexplored p
	If stench or breeze:
		Backtrack until no stench or breeze and an adjacent p is unexplored
If bump, reset p and remove the attempted p from frontier
If gold, backtrack all the way and climb
"""

from Agent import Agent
import random


class MyAI ( Agent ):

	def __init__ ( self ):
		self.p = (0,0)
		self.dx = 1
		self.dy = 0
		self.d = 0 # 0:1,0	1:0,-1	2:-1,0	3:0,1

		self.mapX = -1
		self.mapY = -1
		self.maxX = 0 # Maximum x that it got to
		self.maxY = 0

		self.hasGold = False
		self.numofMoves = 0
		self.moveLimit = 1

		self.stenches = set()
		self.map = set()
		self.frontier = set()
		self.undo = []
		self.tP = (1,0)
		self.tD = 0

		self.backTrack = False
		self.wumpusAlive = True
		self.wumpusPos = False
		self.prepareToShoot = False


	def getAction( self, stench, breeze, glitter, bump, scream ):
		self.numofMoves += 1
		if self.p[0] > self.maxX:
			self.maxX = self.p[0]
		if self.p[1] > self.maxY:
			self.maxY = self.p[1]

		if bump:
			if self.d == 0:
				self.mapX = self.p[0]-1
			if self.d == 3:
				self.mapY = self.p[1]-1
			self.p = (self.p[0]-self.dx,self.p[1]-self.dy)
			self.tP = self.p
			if not self.backTrack:
				del self.undo[0]

		if stench:
			self.stenches.add(self.p)

		self.map.add(self.p)
		if self.p in self.frontier:
			self.frontier.remove(self.p)
		if not (stench and self.wumpusAlive) and not breeze:
			self.addToFrontier()

		if glitter:
			return self.grab()

		if self.p[0] == 0 and self.p[1] == 0 and (self.hasGold or breeze or (stench and self.wumpusAlive)):
			return Agent.Action.CLIMB

		if stench and self.wumpusAlive:
			if self.whereWumpus():
				self.prepareToShoot = True
			else:
				self.backTrack = True
		elif breeze or bump or self.hasGold:
			self.backTrack = True

		if self.prepareToShoot:
			if self.d == self.tD:
				self.wumpusAlive = False
				self.prepareToShoot = False
				return Agent.Action.SHOOT

		elif self.backTrack:
			if not self.hasGold and not (stench and self.wumpusAlive) and not breeze and self.checkAdjacent():
				self.backTrack = False
			elif not self.prepareToShoot and self.p == self.tP and self.d == self.tD:
				if len(self.undo) > 0:
					self.getUndoPosition()
				else:
					self.checkAdjacent()
		else:
			self.checkAdjacent()


		if not self.prepareToShoot and not (self.wumpusPos and self.wumpusAlive) and self.p == self.tP and len(self.undo) > 0:
			self.backTrack = True
			self.getUndoPosition()


		if self.d != self.tD:
			if abs(self.d - self.tD) == 2:
				return self.turnLeft()
			elif self.tD - self.d == -1 or (self.d == 0 and self.tD == 3):
				return self.turnLeft()
			elif self.tD - self.d == 1 or (self.d == 3 and self.tD == 0):
				return self.turnRight()
		elif self.p != self.tP and not self.prepareToShoot:
			return self.forward()

		return Agent.Action.CLIMB


	def getUndoPosition(self):
		self.tP = self.undo.pop(0)
		if self.p[0] < self.tP[0]:
			self.tD = 0
		elif self.p[0] > self.tP[0]:
			self.tD = 2
		elif self.p[1] > self.tP[1]:
			self.tD = 1
		else:
			self.tD = 3


	def addToFrontier(self):
		if self.p[0] > 0 and (self.p[0]-1,self.p[1]) not in self.map:
			self.frontier.add((self.p[0]-1,self.p[1]))
		elif self.p[1] > 0 and (self.p[0],self.p[1]-1) not in self.map:
			self.frontier.add((self.p[0],self.p[1]-1))
		elif (self.mapX == -1 or self.p[0] < self.mapX-1) and (self.p[0]+1,self.p[1]) not in self.map:
			self.frontier.add((self.p[0]+1,self.p[1]))
		elif (self.mapY == -1 or self.p[1] < self.mapY-1) and (self.p[0],self.p[1]+1) not in self.map:
			self.frontier.add((self.p[0],self.p[1]+1))


	def checkAdjacent(self):
		if self.p[0] > 0 and (self.p[0]-1,self.p[1]) not in self.map:
			self.tP = (self.p[0]-1,self.p[1])
			self.tD = 2
			return True

		elif self.p[1] > 0 and (self.p[0],self.p[1]-1) not in self.map:
			self.tP = (self.p[0],self.p[1]-1)
			self.tD = 1
			return True

		elif (self.mapX == -1 or self.p[0] < self.mapX-1) and (self.p[0]+1,self.p[1]) not in self.map:
			self.tP = (self.p[0]+1,self.p[1])
			self.tD = 0
			return True

		elif (self.mapY == -1 or self.p[1] < self.mapY-1) and (self.p[0],self.p[1]+1) not in self.map:
			self.tP = (self.p[0],self.p[1]+1)
			self.tD = 3
			return True
		return False


	def grab(self):
		self.hasGold = True
		return Agent.Action.GRAB


	def whereWumpus(self):
		if len(self.stenches) < 2:
			return False

		if (self.p[0] + 1, self.p[1] - 1) in self.stenches:
			if (self.p[0], self.p[1]-1) in self.map:
				self.tD = 0
				return True
			elif (self.p[0] + 1, self.p[1]) in self.map:
				self.tD = 1
				return True

		elif (self.p[0] - 1, self.p[1] + 1) in self.stenches:
			if (self.p[0], self.p[1]+1) in self.map:
				self.tD = 2
				return True
			elif (self.p[0] - 1, self.p[1]) in self.map:
				self.tD = 3
				return True

		elif (self.p[0] + 1, self.p[1] + 1) in self.stenches:
			if (self.p[0], self.p[1]+1) in self.map:
				self.tD = 0
				return True
			elif (self.p[0] + 1, self.p[1]) in self.map:
				self.tD = 3
				return True

		elif (self.p[0] - 1, self.p[1] - 1) in self.stenches:
			if (self.p[0], self.p[1] - 1) in self.map:
				self.tD = 2
				return True
			elif (self.p[0] - 1, self.p[1]) in self.map:
				self.tD = 1
				return True
		return False


	def forward(self):
		if not self.backTrack:
			self.undo.insert(0,self.p)
		self.p = (self.p[0]+self.dx,self.p[1]+self.dy)
		return Agent.Action.FORWARD


	def turnLeft(self):
		self.d -= 1
		if self.d == -1:
			self.d = 3
		if self.dx == 1:
			self.dx = 0
			self.dy = 1
		elif self.dy == 1:
			self.dx = -1
			self.dy = 0
		elif self.dx == -1:
			self.dx = 0
			self.dy = -1
		else:
			self.dx = 1
			self.dy = 0
		return Agent.Action.TURN_LEFT


	def turnRight(self):
		self.d = (self.d + 1)%4
		if self.dx == 1:
			self.dx = 0
			self.dy = -1
		elif self.dy == 1:
			self.dx = 1
			self.dy = 0
		elif self.dx == -1:
			self.dx = 0
			self.dy = 1
		else:
			self.dx = -1
			self.dy = 0