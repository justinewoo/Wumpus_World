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

		self.map = {}
		self.frontier = []
		self.moveStack = []
		self.undoStack = []
		self.backTrack = False

		self.numofMoves = 0

	def getAction( self, stench, breeze, glitter, bump, scream ):
		if bump:
			self.x -= self.dx
			self.y -= self.dy

		self.numofMoves += 1
		print(self.numofMoves,self.x,self.y)
		self.addToMap(stench,breeze)

		if glitter:
			return self.grab()
		if self.x == 0 and self.y == 0:
			if stench or breeze or self.hasGold:
				print("CLIMB")
				return Agent.Action.CLIMB
			else:
				move = Forward()
				self.moveStack.append(move)


		
		if self.backTrack:
			return self.undoStack.pop(0).action(self)
		else:
			if stench or breeze:
				self.backTrack = True

		if len(self.moveStack) > 0:
			move = self.moveStack.pop(0)
			self.undoStack.append(move)
			return move.action(self)

		if len(self.frontier) > 0:
			coord = self.frontier.pop(0)


	def addToMap(self, stench, breeze):
		if (self.x,self.y) not in self.map:
			self.map[(self.x,self.y)] = not stench and not breeze


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



class Grab:
	def action(self, agent):
		agent.moved = False
		agent.hasGold = True
		print("GOLD===========================================================")
		return Agent.Action.GRAB

class Forward:
	def __init__(self):
		print("ASFASFAS")

	def action(self, agent):
		agent.x += agent.dx
		agent.y += agent.dy
		agent.moved = True
		print("FORWARD")
		return Agent.Action.FORWARD

	def undo(self, agent):
		agent.moveStack.append(TurnLeft())
		agent.moveStack.append(TurnLeft())
		agent.moveStack.append(Foward())


class TurnLeft:
	def action(self, agent):
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
		agent.moved = False
		print("TURN_LEFT")
		return Agent.Action.TURN_LEFT

	def undo(self, agent):
		agent.moveStack.append(TurnRight())


class TurnRight:
	def action(self, agent):
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
		agent.moved = False
		print("TURN_RIGHT")
		return Agent.Action.TURN_RIGHT

	def undo(self, agent):
		agent.moveStack.append(TurnLeft())