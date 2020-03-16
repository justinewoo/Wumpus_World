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

printStuff = False


class MyAI ( Agent ):

	def __init__ ( self ):
		self.x = 0
		self.y = 0
		self.dx = 1
		self.dy = 0
		self.direction = 0 # 0:1,0	1:0,-1	2:-1,0	3:0,1

		self.mapX = -1
		self.mapY = -1
		self.maxX = 0 # Maximum x that it got to
		self.maxY = 0

		self.hasGold = False
		self.numofMoves = 0
		self.moveLimit = 1

		self.map = {}
		self.moves = []
		self.undo = []

		self.backTrack = False


	def getAction( self, stench, breeze, glitter, bump, scream ):
		self.numofMoves += 1

		if self.x > self.maxX:
			self.maxX = self.x
		if self.y > self.maxY:
			self.maxY = self.y


		if len(self.map)*5 > self.moveLimit:
			self.moveLimit = len(self.map)*5


		if bump:
			if self.direction == 0:
				self.mapX = self.x
			if self.direction == 3:
				self.mapY = self.y
			self.x -= self.dx
			self.y -= self.dy

			del self.undo[0:min(5,len(self.undo))]

		self.addToMap(stench, breeze)


		if printStuff:
			self.printStatus()


		if glitter:
			return self.grab()

		if self.x == 0 and self.y == 0 and (self.hasGold or breeze or stench or self.numofMoves > self.moveLimit):
			return Agent.Action.CLIMB


		if not self.backTrack and (stench or breeze or bump):
			self.backTrack = True
			self.moves = []

		if self.backTrack:
			if not stench and not breeze and not bump:
				self.backTrack = not self.checkForUnexplored()

		if (self.backTrack or self.hasGold or self.numofMoves > self.moveLimit) and len(self.undo) > 0:
			return self.undo.pop(0).action(self)

		if not self.backTrack and len(self.moves) == 0:
			# self.checkForUnexplored()
			self.moves.append(Forward())

		if len(self.moves) > 0:
			move = self.moves.pop(0)
			move.undo(self)
			return move.action(self)
		

	def checkForUnexplored(self):
		if (self.mapY == -1 or self.y < self.mapY-1) and (self.x,self.y+1) not in self.map:
			self.setDirection(3)
			return True
		elif self.y > 0 and (self.x,self.y-1) not in self.map:
			self.setDirection(1)
			return True
		elif (self.mapX == -1 or self.x < self.mapX-1) and (self.x+1,self.y) not in self.map:
			self.setDirection(0)
			return True
		elif self.x > 0 and (self.x-1,self.y) not in self.map:
			self.setDirection(2)
			return True
		return False


	def setDirection(self, direction):
		if abs(self.direction - direction) == 2:
			self.moves.append(TurnLeft())
			self.moves.append(TurnLeft())
		elif direction - self.direction == -1 or (self.direction == 0 and direction == 3):
			self.moves.append(TurnLeft())
		elif direction - self.direction == 1 or (self.direction == 3 and direction == 0):
			self.moves.append(TurnRight())


	def addToMap(self, stench, breeze):
		self.map[(self.x,self.y)] = not stench and not breeze


	def grab(self):
		self.moved = False
		self.hasGold = True
		if printStuff:
			print("GOLD===========================================================")
		return Agent.Action.GRAB


	def printStatus(self):
		print("BACKTRACK: " + str(self.backTrack))
		print("MAP: " + str(self.map))
		print("MOVES: " + str(self.moves))
		print("UNDO: " + str(self.undo))
		print("MAPX","MAPY", self.mapX, self.mapY, "X,Y: ",self.x,self.y)


class Forward:
	def action(self, agent):
		agent.x += agent.dx
		agent.y += agent.dy
		if printStuff:
			print("FORWARD")
		return Agent.Action.FORWARD

	def undo(self, agent):
		agent.undo.insert(0,TurnRight())
		agent.undo.insert(0,TurnRight())
		agent.undo.insert(0,Forward())
		agent.undo.insert(0,TurnLeft())
		agent.undo.insert(0,TurnLeft())


class TurnLeft:
	def action(self, agent):
		agent.direction -= 1
		if agent.direction == -1:
			agent.direction = 3
		if agent.dx == 1:
			agent.dx = 0
			agent.dy = 1
		elif agent.dy == 1:
			agent.dx = -1
			agent.dy = 0
		elif agent.dx == -1:
			agent.dx = 0
			agent.dy = -1
		else:
			agent.dx = 1
			agent.dy = 0
		if printStuff:
			print("TURN_LEFT")
		return Agent.Action.TURN_LEFT

	def undo(self, agent):
		agent.undo.insert(0,TurnRight())


class TurnRight:
	def action(self, agent):
		agent.direction = (agent.direction + 1)%4
		if agent.dx == 1:
			agent.dx = 0
			agent.dy = -1
		elif agent.dy == 1:
			agent.dx = 1
			agent.dy = 0
		elif agent.dx == -1:
			agent.dx = 0
			agent.dy = 1
		else:
			agent.dx = -1
			agent.dy = 0
		if printStuff:
			print("TURN_RIGHT")
		return Agent.Action.TURN_RIGHT

	def undo(self, agent):
		agent.undo.insert(0,TurnLeft())