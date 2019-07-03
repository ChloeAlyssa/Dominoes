import numpy as np
import initDomino
import game
import mainDomino
import random
import playersInput
import phrases
#import humanInput
#import minimax

def Random():
	global match, robot, gameTable, play, pickBone, boneyard, gameType, possMove, playerNum, play
	global gameTable1, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7
	game.Turn()
	print game.turn

	if len(game.turn) == 1 or len(game.turn) == 2:
		robot, init = mainDomino.getInitRobot()
		# print init
		gameTable = mainDomino.getInitGameTable()
		# gameTable1 = mainDomino.gameTable1
	elif len(game.turn) == 3 or len(game.turn) == 4:
		robot = mainDomino.robot		
		gameTable = playersInput.gameTable
		# gameTable1 = mainDomino.gameTable1
	else:
		gameTable = playersInput.gameTable
		# gameTable1 = playersInput.gameTable1

	if len(mainDomino.gameTable1) == 2 and len(game.turn) >= 3:
		gameTable1 = playersInput.gameTable1
	else:
		gameTable1 = mainDomino.gameTable1
	if len(mainDomino.gameTable2) > 2:
		gameTable2 = playersInput.gameTable2
	else:
		gameTable2 = mainDomino.gameTable2
	if len(mainDomino.gameTable3) > 2:
		gameTable3 = playersInput.gameTable3
	else:
		gameTable3 = mainDomino.gameTable3
	if len(mainDomino.gameTable4) > 2:
		gameTable4 = playersInput.gameTable4
	else:
		gameTable4 = mainDomino.gameTable4
	if len(mainDomino.gameTable5) > 2:
		gameTable5 = playersInput.gameTable5
	else:
		gameTable5 = mainDomino.gameTable5
	if len(mainDomino.gameTable6) > 2:
		gameTable6 = playersInput.gameTable6
	else:
		gameTable6 = mainDomino.gameTable6
	if len(mainDomino.gameTable7) > 2:
		gameTable7 = playersInput.gameTable7
	else:
		gameTable7 = mainDomino.gameTable7

	#elif init == False:
    	## We want this one if its not coming from init
	# robot = mainDomino.robot
	# if len(robot)<6:
		# robot = mainDomino.UpdateRobot()
	# gameTable = mainDomino.gameTable

	phrases.supportive("robotsTurn")
	#phrases.competitive("robotsTurn")
	
	Matching()

	play = []
	robotPlay = []

	# if initDomino.playerNum == 1:
	# 	boneyard = mainDomino.boneyard
	# else:
	# 	player2 = mainDomino.player2
	# 	player3 = mainDomino.player3

	#gameType = initDomino.gameType

	# if there is one match then play it	
	# print("match = ")
	# print match
	if len(match) == 2:
		robotPlay = match
		# play = [int(play) for play in play]
	# if there are more than one match, randomly pick one to play

	elif len(match) >= 4:
		i = len(match)/2

		possMove = np.resize(match, (i, 2))
		match = random.sample(possMove, 1)
		robotPlay = np.resize(match, (1,2))


	elif len(match) == 0:
		while match == []:
			i = len(robot)+1
			if len(mainDomino.boneyard)>0:
				initDomino.asr.say("I need a tile from the boneyard please")
				mainDomino.robotsTiles()
				pickBone = mainDomino.bar
				robot = np.append(pickBone, robot)
				robot = np.reshape(robot, (i,2))
				RemoveBoneyard()
				mainDomino.UpdateBoneyard()
				mainDomino.UpdateRobot()
				Random()
			elif len(boneyard) == 0: # if there are no more tiles in boneyard	
				turn = game.Turn() # get next players turn
				if initDomino.playerNum == 1:
					print("boneyard empty, player1's turn")
					playersInput.player1sTurn() # player1s turn
				else:
					print("next players turn")
					playersInput.fourPlayer() # otherwise its the next persons go
	
	# print("here")

	play = np.append(robotPlay, play)

	Remove()
	mainDomino.Doubles()
	whereToPlace()

	Place() # place tile on gameTable
	# print("here!!!!!")

	numCards = str(len(robot))
	#print("I have " + numCards + " cards left")
	# mainDomino.UpdateGame()
	game.GameStatus()
	# print robot
	# game.Turn()

	if initDomino.playerNum == 1:
		playersInput.player1sTurn()
	else:
		playersInput.fourPlayer()

# # Checking if we have any tiles that match on the gametable # # 
def Matching():
	global match, robot, gameTable, gameTable1

	index = 0
	match = []

	for i in range(len(robot)):
		if robot[index,0] == gameTable[0] or robot[index,0] == gameTable[-1]:
			match = np.append(match, robot[index])
		elif robot[index,1] == gameTable[0] or robot[index,1] == gameTable[-1]:
			match = np.append(match, robot[index])
		index+=1

	if len(gameTable1) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable1[0] or robot[index,0] == gameTable1[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable1[0] or robot[index,1] == gameTable1[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable2) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable2[0] or robot[index,0] == gameTable2[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable2[0] or robot[index,1] == gameTable2[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable3) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable3[0] or robot[index,0] == gameTable3[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable3[0] or robot[index,1] == gameTable3[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable4) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable4[0] or robot[index,0] == gameTable4[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable4[0] or robot[index,1] == gameTable4[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable5) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable5[0] or robot[index,0] == gameTable5[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable5[0] or robot[index,1] == gameTable5[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable6) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable6[0] or robot[index,0] == gameTable6[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable6[0] or robot[index,1] == gameTable6[-1]:
				match = np.append(match, robot[index])
			index+=1

	if len(gameTable7) != 0:
		index = 0
		for i in range(len(robot)):
			if robot[index,0] == gameTable7[0] or robot[index,0] == gameTable7[-1]:
				match = np.append(match, robot[index])
			elif robot[index,1] == gameTable7[0] or robot[index,1] == gameTable7[-1]:
				match = np.append(match, robot[index])
			index+=1

	# return

# # Removing tile from hand # # 
def Remove():
	global robot, play, indx

	indx = 0
	for i in range(len(robot)):
		if robot[indx,0] == play[0] and robot[indx,1] == play[1]:
			robot = np.delete(robot, [indx],0) # remove played tile from hand
		else:				
			indx+=1
	mainDomino.pointAt()

# Function to decide where to place tile 
def whereToPlace():
	global play, gameTable, gameTable1, where, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7
	where = 0
	if len(mainDomino.gameTable1) != 0:
		# if gameTable[0] == gameTable1[0] or gameTable[-1] == gameTable1[-1] or gameTable[0] == gameTable1[-1] or gameTable[-1] == gameTable1[0]:
		if play[0] == gameTable[0] or play[1] == gameTable[0] or play[0] == gameTable[-1] or play[1] == gameTable[-1]:
			print("play on gameTable")
			where = 0
		elif play[0] == gameTable1[0] or play[1] == gameTable1[0] or play[0] == gameTable1[-1] or play[1] == gameTable1[-1]:
			print("play on gameTable1")
			where = 1
		elif len(mainDomino.gameTable2) != 0:
			if play[0] == gameTable2[0] or play[1] == gameTable2[0] or play[0] == gameTable2[-1] or play[1] == gameTable2[-1]:
				print("play on gameTable2")
				where = 2
			elif len(mainDomino.gameTable3) != 0:
				if play[0] == gameTable3[0] or play[1] == gameTable3[0] or play[0] == gameTable3[-1] or play[1] == gameTable3[-1]:
					print("play on gameTable3")
					where = 3
				elif len(mainDomino.gameTable4) != 0:
					if play[0] == gameTable4[0] or play[1] == gameTable4[0] or play[0] == gameTable4[-1] or play[1] == gameTable4[-1]:
						print("play on gameTable4")
						where = 4
					elif len(mainDomino.gameTable5) != 0:
						if play[0] == gameTable5[0] or play[1] == gameTable5[0] or play[0] == gameTable5[-1] or play[1] == gameTable5[-1]:
							print("play on gameTable5")
							where = 5
						elif len(mainDomino.gameTable6) != 0:
							if play[0] == gameTable6[0] or play[1] == gameTable6[0] or play[0] == gameTable6[-1] or play[1] == gameTable6[-1]:
								print("play on gameTable6")
								where = 6
							elif len(mainDomino.gameTable7) != 0:
								if play[0] == gameTable7[0] or play[1] == gameTable7[0] or play[0] == gameTable7[-1] or play[1] == gameTable7[-1]:
									print("play on gameTable7")
									where = 7

def Place(): # place tile next to valid tile on the game table
	global play, gameTable, gameTable1, where, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7

	# play = initDom.play
	# if len(mainDomino.gameTable1) != 0:
	# 	if play[0] == gameTable1[0]: 
	# 		play = play[::-1]
	# 		gameTable1 = np.insert(gameTable1,0,play)
	# 	elif play[0] == gameTable1[-1]:
	# 		gameTable1 = np.insert(gameTable1,len(gameTable1),play)
	# 	elif play[1] == gameTable1[0]:
	# 		gameTable1 = np.insert(gameTable1,0,play)
	# 	elif play[1] == gameTable1[-1]:
	# 		play = play[::-1]
	# 		gameTable1 = np.insert(gameTable1,len(gameTable1),play)
	# 	print gameTable1
	if where == 0:
		if play[0] == gameTable[0]: 
			play = play[::-1]
			gameTable = np.insert(gameTable,0,play)
		elif play[0] == gameTable[-1]:
			gameTable = np.insert(gameTable,len(gameTable),play)
		elif play[1] == gameTable[0]:
			gameTable = np.insert(gameTable,0,play)
		elif play[1] == gameTable[-1]:
			play = play[::-1]
			gameTable = np.insert(gameTable,len(gameTable),play)
		print("GameTable:"); print gameTable
	elif where == 1:
		if play[0] == gameTable1[0]: 
			play = play[::-1]
			gameTable1 = np.insert(gameTable1,0,play)
		elif play[0] == gameTable1[-1]:
			gameTable1 = np.insert(gameTable1,len(gameTable1),play)
		elif play[1] == gameTable1[0]:
			gameTable1 = np.insert(gameTable1,0,play)
		elif play[1] == gameTable1[-1]:
			play = play[::-1]
			gameTable1 = np.insert(gameTable1,len(gameTable1),play)
		print("GameTable1:"); print gameTable1
	elif where == 2:
		if play[0] == gameTable2[0]: 
			play = play[::-1]
			gameTable2 = np.insert(gameTable1,0,play)
		elif play[0] == gameTable2[-1]:
			gameTable2 = np.insert(gameTable2,len(gameTable2),play)
		elif play[1] == gameTable2[0]:
			gameTable2 = np.insert(gameTable2,0,play)
		elif play[1] == gameTable2[-1]:
			play = play[::-1]
			gameTable2 = np.insert(gameTable2,len(gameTable2),play)
		print("GameTable2:"); print gameTable2

	elif where == 3:
		if play[0] == gameTable3[0]: 
			play = play[::-1]
			gameTable3 = np.insert(gameTable3,0,play)
		elif play[0] == gameTable3[-1]:
			gameTable3 = np.insert(gameTable3,len(gameTable3),play)
		elif play[1] == gameTable3[0]:
			gameTable3 = np.insert(gameTable3,0,play)
		elif play[1] == gameTable3[-1]:
			play = play[::-1]
			gameTable3 = np.insert(gameTable3,len(gameTable3),play)
		print("GameTable3:"); print gameTable3

	elif where == 4:
		if play[0] == gameTable4[0]: 
			play = play[::-1]
			gameTable4 = np.insert(gameTable4,0,play)
		elif play[0] == gameTable4[-1]:
			gameTable4 = np.insert(gameTable4,len(gameTable4),play)
		elif play[1] == gameTable4[0]:
			gameTable4 = np.insert(gameTable4,0,play)
		elif play[1] == gameTable4[-1]:
			play = play[::-1]
			gameTable4 = np.insert(gameTable4,len(gameTable4),play)
		print("GameTable4:"); print gameTable4

	elif where == 5:
		if play[0] == gameTable5[0]: 
			play = play[::-1]
			gameTable5 = np.insert(gameTable5,0,play)
		elif play[0] == gameTable5[-1]:
			gameTable5 = np.insert(gameTable5,len(gameTable5),play)
		elif play[1] == gameTable5[0]:
			gameTable5 = np.insert(gameTable5,0,play)
		elif play[1] == gameTable5[-1]:
			play = play[::-1]
			gameTable5 = np.insert(gameTable5,len(gameTable5),play)
		print("GameTable5:"); print gameTable5

	elif where == 6:
		if play[0] == gameTable6[0]: 
			play = play[::-1]
			gameTable6 = np.insert(gameTable6,0,play)
		elif play[0] == gameTable6[-1]:
			gameTable6 = np.insert(gameTable6,len(gameTable6),play)
		elif play[1] == gameTable6[0]:
			gameTable6 = np.insert(gameTable6,0,play)
		elif play[1] == gameTable6[-1]:
			play = play[::-1]
			gameTable6 = np.insert(gameTable6,len(gameTable6),play)
		print("GameTable6:"); print gameTable6

	elif where == 7:
		if play[0] == gameTable7[0]: 
			play = play[::-1]
			gameTable7 = np.insert(gameTable7,0,play)
		elif play[0] == gameTable7[-1]:
			gameTable7 = np.insert(gameTable7,len(gameTable7),play)
		elif play[1] == gameTable7[0]:
			gameTable7 = np.insert(gameTable7,0,play)
		elif play[1] == gameTable7[-1]:
			play = play[::-1]
			gameTable7 = np.insert(gameTable7,len(gameTable7),play)
		print("GameTable7:"); print gameTable7
       
	# return gameTable


def RemoveBoneyard():
	global boneyard, pickBone

	x = len(boneyard) - 1
	boneyard = [None]*x

	return

