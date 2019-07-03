import numpy as np
import initDomino
import game
import mainDomino
import random
import robotPlay
#import minimax

# # # # # # # # # # # # # # # # # # # # Human input # # # # # # # # # # # # # # # # # # # #
def HumansTurn():
	global human, gameTable, play, pickBone, boneyard, gameType, turn

	turn = mainDomino.turn
	#boneyard = main.boneyard
	play = []
	humanPlay = mainDomino.humanPlay
	print humanPlay
##	while True:
##
##                humanPlay = mainDomino.humanPlay # input the tile you want to play
##                if humanPlay == "pass" or humanPlay == "00":
##                        break
##                else:
##                        humanPlay = int(humanPlay)
##                        break

	boneyard = mainDomino.boneyard

	if humanPlay == "pass":
		i = len(human) + 1
		print("i = " + str(i))
		if len(boneyard)>0:
			pickBone = random.sample(boneyard, 1)
			human = np.append(pickBone, human)
			human = np.reshape(human, (i,2))
			print("New hand = ")
			print human
			RemoveBoneyard()
			main.UpdateBoneyard()
			main.UpdateHuman()
			if boneyard == []:
				print("boneyard empty, next players turn")
				robotPlay.Random()
			HumansTurn() 
	elif humanPlay == "00":
		play =  np.zeros(2)
	else:
		#humanPlay = int(humanPlay)
		#humanPlay = [int(i) for i in str(humanPlay)]
		play = np.append(humanPlay, play)
        print("play = ")
	print play
	#Remove() # remove played tile from hand

	Place() # place tile on gameTable

def Remove():
	global human, play

	# human = main.human
	
	# play = game.play
	if initDomino.playerNum == 1:
		indx = 0
		for i in range(len(human)):
			if human[indx,0] == play[0] and human[indx,1] == play[1]:
				human = np.delete(human, [indx],0) # remove played tile from hand
				print human
			else:				
				indx+=1
	elif initDom.playerNum == 3:
		indx = 0
		if main.turn[0] == 1:
			for i in range(len(human)):
				if human[indx,0] == play[0] and human[indx,1] == play[1]:
					human = np.delete(human, [indx],0) # remove played tile from hand
					print human
				else:				
					indx+=1
		if main.turn[0] == 2:
			for i in range(len(human2)):
				if human2[indx,0] == play[0] and human2[indx,1] == play[1]:
					human2 = np.delete(human2, [indx],0) # remove played tile from hand
					print human2
				else:				
					indx+=1
		elif main.turn[0] == 3:
			for i in range(len(human2)):
				if human3[indx,0] == play[0] and human3[indx,1] == play[1]:
					human3 = np.delete(human3, [indx],0) # remove played tile from hand
					print human3
				else:				
					indx+=1
	return

def Human4():
	global human, gameTable, play, pickBone, boneyard, gameType, turn, human2, human3

	turn = main.turn
	human = main.human
	human2 = main.human2
	human3 = main.human3
	play = []	
	game.GameStatus()
	
	while True:
		try:
			humanPlay = raw_input('*** input tile *** ') # input the tile you want to play
			if humanPlay == "pass" or humanPlay == "00":
				break
			else:
				humanPlay = int(humanPlay)
				break
		except ValueError:
			print("Whoops, try typing it again...")

	if humanPlay == "pass":
		# goes to the next person
		game.Turn()
		print("turn = ")
		print turn
	elif humanPlay == "00":
		play =  np.zeros(2)
	else:
		humanPlay = int(humanPlay)
		humanPlay = [int(i) for i in str(humanPlay)]
		play = np.append(humanPlay, play)

	Remove() # remove played tile from hand

	Place() # place tile on gameTable

def Place():
	global play, gameTable

	gameTable = mainDomino.gameTable
        print "Game table"
        print gameTable
	# play = initDom.play

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

	print gameTable
	mainDomino.UpdateGame()
	game.GameStatus()
	# if initDom.gameType == 1:
	robotPlay.Random()
	# elif initDom.gameType == 2:
	# 	minimax.MiniMax()


def RemoveBoneyard():
	global boneyard, pickBone

	# boneyard = main.boneyard
	# pickBone = initDom.pickBone
	
	indx = 0
	for i in range(len(boneyard)):
		if np.all(boneyard[indx] == pickBone): 
			boneyard = np.delete(boneyard, [indx],0) # remove played tile from hand
		else:				
			indx+=1
	return

def Matching():
	global match, human, gameTable

	gameTable = main.gameTable

	human = main.human

	index = 0
	match = []

	for i in range(len(human)):
		if human[index,0] == gameTable[0] or human[index,0] == gameTable[-1]:
			match = np.append(match, human[index])
		elif human[index,1] == gameTable[0] or human[index,1] == gameTable[-1]:
			match = np.append(match, human[index])
		index+=1
	return

