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

		self.hasGold = False

		self.map = []

		self.numofmoves = 0

	def getAction( self, stench, breeze, glitter, bump, scream ):
		self.numofmoves += 1
		print(self.numofmoves,self.x,self.y)

		if glitter and not self.hasGold:
			return self.grab()
		if self.x == 0 and self.y == 0:
			if stench or breeze or self.hasGold:
				print("CLIMB")
				return Agent.Action.CLIMB

		if bump:
			self.x -= self.dx
			self.y -= self.dy

		return self.forward()


	def isForwardSafe(self):
		return (self.x + self.dx, self.y + self.dy) in self.safe and self.safe[(self.x + self.dx, self.y + self.dy)]


	def addToMap(self, stench, breeze):
		if len(self.map) <= self.x:
			self.map.append([])
		if len(self.map[self.x]) <= self.y:
			self.map[self.x].append((stench,breeze))
		if not stench and not breeze and (self.x,self.y) not in self.safe:
			self.safe[(self.x,self.y)] = not stench and not breeze


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
