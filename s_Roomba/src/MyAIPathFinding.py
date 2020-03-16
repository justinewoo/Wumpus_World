# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
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

from Agent import Agent
import random

class MyAI ( Agent ):

	def __init__ ( self ):
		self.x = 0
		self.y = 0
		self.dx = 1
		self.dy = 0
		self.direction = 0 # 0:1,0	1:0,-1	2:-1,0	3:0,1

		self.hasGold = False

		self.frontier = []
		self.map = {}
		self.moves = []

		self.numofMoves = 0


	def getAction( self, stench, breeze, glitter, bump, scream ):
		if glitter:
			return self.grab()
		if self.x == 0 and self.y == 0 and (self.hasGold or breeze or stench):
			return Agent.Action.CLIMB

		self.addToFrontier(self.x, self.y)
		print(self.frontier)
		if len(self.frontier) > 0:
			coord = self.frontier.pop(0)
			self.addPath(coord[0], coord[1])

		if len(self.moves) > 0:
			return self.moves.pop(0)
			

	def addPath(self, x, y):
		# Recursively find a path to the goal
		self.addPathL(x,y,set((x,y)),0)


	def addPathL(self, x, y, checked, num):
		num += 1
		if num > 49:
			return False
		if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
			return True

		if (x-1,y) in self.map and (x-1,y) not in checked:
			checked.add((x-1,y))
			if self.addPathL(x-1,y,checked,num):
				# self.fuckToWork(x,y,x-1,y)
				return True

		if (x+1,y) in self.map and (x+1,y) not in checked:
			checked.add((x+1,y))
			if self.addPathL(x+1,y,checked,num):
				return True

		if (x,y-1) in self.map and (x,y-1) not in checked:
			checked.add((x,y-1))
			if self.addPathL(x,y-1,checked,num):
				return True

		if (x,y-1) in self.map and (x,y-1) not in checked:
			checked.add((x,y-1))
			if self.addPathL(x,y-1,checked,num):
				return True


	def fuckToWork(self, x, y, x2, y2):
		pass


	def addToFrontier(self, x, y):
		if (x+1,y) not in self.map and (x+1,y) not in self.frontier:
			self.frontier.append((x+1,y))
		if (x,y+1) not in self.map and (x,y+1) not in self.frontier:
			self.frontier.append((x,y+1))
		if x > 0:
			if (x-1,y) not in self.map and (x-1,y) not in self.frontier:
				self.frontier.append((x-1,y))
		if y > 0:
			if (x,y-1) not in self.map and (x,y-1) not in self.frontier:
				self.frontier.append((x,y-1))


	def addToMap(self, stench, breeze):
		self.map[(self.x,self.y)] = not stench and not breeze

	def grab(self):
		self.moved = False
		self.hasGold = True
		print("GOLD===========================================================")
		return Agent.Action.GRAB


	def shoot(self):
		self.moved = False
		print("SHOOT")
		return Agent.Action.SHOOT


	def forward(self):
		self.x += self.dx
		self.y += self.dy
		self.moved = True
		print("FORWARD")
		return Agent.Action.FORWARD


	def turnLeft(self):
		self.direction -= 1
		if self.direction == -1:
			self.direction = 3
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
		self.moved = False
		print("TURN_LEFT")
		return Agent.Action.TURN_LEFT


	def turnRight(self):
		self.direction = (self.direction + 1)%4
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
		self.moved = False
		print("TURN_RIGHT")
		return Agent.Action.TURN_RIGHT


	def printStatus(self):
		print("----------------")
		for col in self.map:
			for square in col:
					tempStr = ""
					if square[0]:
						tempStr += "S"
					else:
						tempStr += " "
					if square[1]:
						tempStr += "B"
					else:
						tempStr += " "
					print("|" + tempStr + "|",end="")
			print()
			print(self.map)
		print("---------------")
