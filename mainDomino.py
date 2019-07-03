import initDomino
# from robotRandom import *
# from minimax import *
# from gameStatus import *
#import game
import robotPlay
import playersInput
import random
#import minimax
import numpy as np
import Start
import game
import barcodeScanner
import time
#import almath
# Uncomment for robot
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker

myBroker = ALBroker("myBroker", "0.0.0.0", 0, "Mario.local", 9559)
asr = ALProxy("ALAnimatedSpeech")
config = {"bodyLanguageMode":"contextual"}
motion = ALProxy("ALMotion")
global speech
speech = ALProxy("ALSpeechRecognition")
global memory
memory = ALProxy("ALMemory")

def InitGame():
	global player1, robot, boneyard, gameTable, turn, player2, player3, playerNum, start, player1Play
	global gameTable1, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7, StartUp
	robot = initDomino.robot
	player1 = initDomino.player1
	#print player1Play
	gameTable1 = []
	gameTable2 = []
	gameTable3 = []
	gameTable4 = []
	gameTable5 = []
	gameTable6 = []
	gameTable7 = []
	if initDomino.start == 0:
		gameTable = initDomino.gameTable
		game.Turn()
	elif initDomino.start == 1: #THIS NEEDS CHANGING
		print gameTable
	# turn = []
	if initDomino.playerNum == 1:
		boneyard = initDomino.boneyard
	else:
		player2 = initDomino.player2
		player3 = initDomino.player3
	whoStarts()

	#return robot, gameTable
# def one():
# 	global playerNum
# 	playerNum = 1
# 	main()

# def four():
# 	global playerNum
# 	playerNum = 3
# 	main()

################## Function to call the barcode scanner to get robots hand ##################
def robotsTiles():
	global cameraNo, bar, init, posBar

	cameraNo = 1
	# barcodeScannerVideo.main()
	if initDomino.init:
		barcodeScanner.Scan("deal") # scan for barcodes
	else:
		barcodeScanner.Scan("boneyard") # scan for barcodes
	bar = barcodeScanner.bar # hand taken from barcode scanner and put into an array
	posBar = barcodeScanner.posBar # position of barcodes
	#bar = barcodeScanner.bar # hand taken from barcode scanner and put into an array
	#posBar = barcodeScanner.posBar # position of barcodes
	
	bar = np.array(bar)

	return bar, posBar

def showTile():
	global player1Play
	barcodeScanner.Scan("unsure")
	player1Play = barcodeScanner.bar
	initDomino.asr.say("I see" + str(player1Play))
	playersInput.carryOn()

def playerPass():
	global player1Play
	player1Play = "pass"

def whoStarts():
	global playerNum, start, init
	# game.Turn() # gets whose turn it is 
	# init = initDomino.init
	# print("right"); print init
	# init = False
	if initDomino.playerNum == 1: # if robot doesn't start, 2 player  
		if initDomino.start == 1:
			robotPlay.Random()
		else:
			# game.Turn()
			# print init, game.turn
			playersInput.player1sTurn()
	elif initDomino.playerNum == 3: # if robot doesn't start, 4 player
		playersInput.fourPlayer()
	#elif initDomino.start == 0: # if robot starts
		#robotPlay.Random()
		
def getInitRobot():
        global init, robot
        print("getInitRobot")
        robot = initDomino.robot
        # print robot[0]
        # print("IM HERE")
        game.Turn()
        init = False

        return robot, init

def getInitGameTable():
		global gameTable, start
		print("getInitGameTable")
		# if start == 0:
		# 	gameTable = initDomino.gameTable
		# elif start == 1:
		# 	print("here")
		# 	gameTable = Start.gameTable

		print gameTable
        # init = False
		return gameTable

def UpdateBoneyard():
	global boneyard, turn

	if turn[0] == 1:
		boneyard = robotPlay.boneyard
	else:
		boneyard = playersInput.boneyard
	return boneyard

def MatchingBoneyard():
	global match, boneyard, gameTable

	# gameTable = main.gameTable

	# player1 = main.player1

	index = 0
	match = []

	for i in range(len(boneyard)):
		if boneyard[index,0] == gameTable[0] or boneyard[index,0] == gameTable[-1]:
			match = np.append(match, boneyard[index])
		elif boneyard[index,1] == gameTable[0] or boneyard[index,1] == gameTable[-1]:
			match = np.append(match, boneyard[index])
		index+=1
	return match

def UpdateRobot():
	global robot, start
	robot = robotPlay.robot
	# gameTable
	return robot

def UpdateGame():
	global turn, nextPlayer, gameTable, player1, robot
	# depending on who's go it is
	# update gameTable
	init = False

	turn = game.turn
	if initDomino.playerNum == 1:
		if turn[0] == 1:
			nextPlayer = 0
			if initDomino.start != 1:
				gameTable = playersInput.gameTable
				player1 = playersInput.player1
			#return
		elif turn[0] == 0:
			nextPlayer = 1
			gameTable = robotPlay.gameTable
			robot = robotPlay.robot
			# minimax.PossibleMoves()
	elif initDomino.playerNum == 3:
		if turn[0] !=0:
			gameTable = playersInput.gameTable
			if turn[0] == 1:
				nextPlayer = 2
				player1 = playersInput.player1
			if turn[0] == 2:
				nextPlayer = 3
				player2 = playersInput.player2
			if turn[0] == 3:
				nextPlayer = 0
				player3 = playersInput.player3
		else:
			gameTable = robotPlay.gameTable

		
	# return gameTable

def Round(x, base=5):
    return int(base * round(float(x)/base))

def Doubles():
    global d1, maxi, robot, double, play
    global gameTable, gameTable1, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7

    double = False
    # print("HERE")
    # print gameTable
    if game.turn[0] == 1:
    	# gameTable = playersInput.gameTable
    	play = playersInput.play
    else:
    	# gameTable = robotPlay.gameTable
    	play = robotPlay.play
    # # index = 0
    # checks for doubles
    # for i in range(len(player1Play)):
    # if player1Play[0] == player1Play[1] or robotPlay[0] == robotPlay[1]:
        # double.append(player1Play)
        # double = True
    if play[0] == play[1]:
		print("Double!!")

		# if len(gameTable) != 0:
			# print("gameTable:")
			# print gameTable
		if len(gameTable1) == 0:
			gameTable1 = np.append(gameTable1, play)
			print("gameTable1:")
			print gameTable1
		elif len(gameTable2) == 0:
			gameTable2 = np.append(gameTable2, play)
			print("gameTable2:")
			print gameTable2
		elif len(gameTable3) == 0:
			gameTable3 = np.append(gameTable3, player1Play)
			print("gameTable3:")
			print gameTable3
		elif len(gameTable4) == 0:
			gameTable4 = np.append(gameTable4, player1Play)
			print("gameTable4:")
			print gameTable4
		elif len(gameTable5) == 0:
			gameTable5 = np.append(gameTable5, player1Play)
			print("gameTable5:")
			print gameTable5
		elif len(gameTable6) == 0:
			gameTable6 = np.append(gameTable6, player1Play)
			print("gameTable6:")
			print gameTable6
		elif len(gameTable7) == 0:
			gameTable7 = np.append(gameTable7, player1Play)
			print("gameTable7:")
			print gameTable7


def playersTile():
    global cameraNo, bar, player1Play, player2Play, player3Play, init
    global gameTable
    #cameraNo = 0

    # init = False
    # barcodeScanner.Scan()
    # print game.turn
    if game.turn[0] == 1:
    	initDomino.speech.subscribe("domPlayedRecognised")
    	time.sleep(2)
    	initDomino.memory.subscribeToEvent("WordRecognized", "StartUp", "domPlayedRecognised")
    	initDomino.speech.unsubscribe("domPlayedRecognised")
    	# player1Play = raw_input("*** Player 1 input tile ***")
    	# player1Play = int(player1Play)
    	# player1Play = [int(i) for i in str(player1Play)]
    	#player1Play = barcodeScanner.bar
    	# player1Play = barcodeScannerVideo.bar
    elif game.turn[0] == 2:
    	player2Play = raw_input("*** Player 2 input tile ***")
    	player2Play = int(player1Play)
    	player2Play = [int(i) for i in str(player1Play)]
    	#player2Play = barcodeScanner.bar
    	# player2Play = barcodeScannerVideo.bar
    elif game.turn[0] == 3:
    	player3Play = raw_input("*** Player 3 input tile ***")
    	player3Play = int(player1Play)
    	player3Play = [int(i) for i in str(player1Play)]
    	#player3Play = barcodeScanner.bar
    	# player3Play = barcodeScannerVideo.bar

def zeroZero():
	global player1Play
	player1Play = [0, 0]
	heardTiles()
def zeroOne():
	global player1Play
	player1Play = [0, 1]
	heardTiles()
def zeroTwo():
	global player1Play
	player1Play = [0, 2]
	heardTiles()
def zeroThree():
	global player1Play
	player1Play = [0, 3]
	heardTiles()
def zeroFour():
	global player1Play
	player1Play = [0, 4]
	heardTiles()
def zeroFive():
	global player1Play
	player1Play = [0, 5]
	heardTiles()
def zeroSix():
	global player1Play
	player1Play = [0, 6]
	heardTiles()
def oneOne():
	global player1Play
	player1Play = [1, 1]
	heardTiles()
def oneTwo():
	global player1Play
	player1Play = [1, 2]
	heardTiles()
def oneThree():
	global player1Play
	player1Play = [1, 3]
	heardTiles()
def oneFour():
	global player1Play
	player1Play = [1, 4]
	heardTiles()
def oneFive():
	global player1Play
	player1Play = [1, 5]
	heardTiles()
def oneSix():
	global player1Play
	player1Play = [1, 6]
	heardTiles()
def twoTwo():
	global player1Play
	player1Play = [2, 2]
	heardTiles()
def twoThree():
	global player1Play
	player1Play = [2, 3]
	heardTiles()
def twoFour():
	global player1Play
	player1Play = [2, 4]
	heardTiles()
def twoFive():
	global player1Play
	player1Play = [2, 5]
	heardTiles()
def twoSix():
	global player1Play
	player1Play = [2, 6]
	heardTiles()
def threeThree():
	global player1Play
	player1Play = [3, 3]
	heardTiles()
def threeFour():
	global player1Play
	player1Play = [3, 4]
	heardTiles()
def threeFive():
	global player1Play
	player1Play = [3, 5]
	heardTiles()
def threeSix():
	global player1Play
	player1Play = [3, 6]
	heardTiles()
def fourFour():
	global player1Play
	player1Play = [4, 4]
	heardTiles()
def fourFive():
	global player1Play
	player1Play = [4, 5]
	heardTiles()
def fourSix():
	global player1Play
	player1Play = [4, 6]
	heardTiles()
def fiveFour():
	global player1Play
	player1Play = [5, 4]
	heardTiles()
def fiveFive():
	global player1Play
	player1Play = [5, 5]
	heardTiles()
def fiveSix():
	global player1Play
	player1Play = [6, 6]
	heardTiles()

def heardTiles():
	global speech, memory
	initDomino.speech.subscribe("speechTest")
	initDomino.memory.subscribeToEvent("WordRecognized", "StartUp", "correctIncorrectRecognised")
	initDomino.speech.unsubscribe("speechTest")


def updateGameTable():
	global player1Play, gameTable
	if init:
		gameTable=[]
		gameTable = np.append(gameTable, player1Play)
		InitGame()
	# else:
	# 	gameTable = robotPlay.gameTable

def pointAt():
	global indx, posture
	initDomino.posture.goToPosture("StandInit", 0.5)
	if initDomino.init:
		pixCoord = posBar[initDomino.indx]
	else:
		pixCoord = posBar[robotPlay.indx]
	pixCoord = np.reshape(pixCoord, (1,3))
	y = pixCoord[0,0] / 4200.0 # 4200 pixels per meter
	z = pixCoord[0,1] / 4200.0 
	x = 0.23 # tiles are 0.26m away from nao's torso
	motion = ALProxy("ALMotion")
	effector   = "RArm"
	frame      = 0 # FRAME_TORSO
	# axisMask   = almath.AXIS_MASK_VEL # just control position
	# useSensorValues = False

	# path = []
	# currentTf = motion.getTransform(effector, frame, useSensorValues)
	# targetTf  = almath.Transform(currentTf)
	# targetTf.r1_c4 = x # x
	# targetTf.r2_c4 = y # y
	# targetTf.r3_c4 = z # z

	# path.append(list(targetTf.toVector()))
	# path.append(currentTf)
	# print path

	# # Go to the target and back again
	# times      = [2.0, 4.0] # seconds
	
	initDomino.asr.say("I would like to play", initDomino.config)
	initDomino.tracker.pointAt(effector, [x, y, z], frame, 0.5)
	initDomino.asr.say("this tile", initDomino.config)
	print("I would like to play this tile.")
	
	# motion.transformInterpolations(effector, frame, path, axisMask, times)
	#motion.openHand("RHand")

def main():
	global player1, robot, boneyard, gameTable, turn, gameType, init, playerNum, player1Play
	init = True
# # # # # # # # # # # Change number of players here # # # # # # # # # # #
	playerNum = 1
	player1Play = []
	# playerNum = 3
	# print("Hello, my name is NAO")

	initDomino.main() # starts initilising the game
	#print("herere")
	#InitGame() #   

if __name__ == "__main__":
    main()
