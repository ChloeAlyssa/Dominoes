#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import initDomino
import numpy as np
import game
import random
import mainDomino
import barcodeScanner
import robotPlay
import playersInput
import phrases
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "Mario.local"

sys.argv = ['']

# Global variable to store the StartUp module instance
StartUp = None
memory = None
speech = None
face = None
tracker = None
motion = None
posture = None
asr = None
aware = None
life = None
config = None
wordRecog = None
#gameTable = []
#global gameTable
play = []
playerNum = None
start = None
#elf.playerNum = None
			

class StartUpModule(ALModule):
# A simple module able to react
#to facedetection events

	def __init__(self, name):
		ALModule.__init__(self, name)

        # Setting up proxies
		try:
			global speech, face, tracker, memory, motion, posture, asr, aware, gameTable, player1Play, vct
			gameTable = []
			player1Play = []
			vct = phrases.vct
			print("Connecting to proxies ...")
			self.tts = ALProxy("ALTextToSpeech")
			speech = ALProxy("ALSpeechRecognition")
			face = ALProxy("ALFaceDetection")
			tracker = ALProxy("ALTracker")
			memory = ALProxy("ALMemory")
			motion = ALProxy("ALMotion")
			posture= ALProxy("ALRobotPosture")
			asr = ALProxy("ALAnimatedSpeech")
			aware = ALProxy("ALBasicAwareness")
			life = ALProxy("ALAutonomousLife")
			leds = ALProxy("ALLeds")
		except:
			print("Error creating proxies")

        # Sets a list of vocabulary that should be recognised
		try:
			print("Setting vocab ...")
			speech.setLanguage("English")
			vocab = ["hello", "zero", "one", "two", "three", "four", "five", "six" "yes", "no", "Mario", "you", "I", "yes", "pass"]
			speech.setVocabulary(vocab, True)
			#barcodeScanner.Scan("begin")
		except:
			print("Can't set vocab")

        # Set visual expression to show nao is listening and enable face tracking
		try:
			print("Setting up visual expression and tracking ...")
			speech.setVisualExpression(True)
			motion.wakeUp()
			# if competitive:
			# 	leds.on('AllLedsRed')
			# else:
			# 	leds.on('AllLedsGreen')
			#motion.setStiffnesses("Body", 1.0)
			#posture.goToPosture("Stand", 0.5)
			# Add target to track.
			targetName = "Face"
			faceWidth = 0.1 # default
			tracker.registerTarget(targetName, faceWidth)
			tracker.track(targetName)
		except:
			print("Visual expression and/or tracking aren't working")

        # Subscribe to the FaceDetected event
		try:
			print("Subscribing to events ...")
			memory.subscribeToEvent("FaceDetected", "StartUp", "onFaceDetected")
			playerNum = None

		except:
			print("Can't subscribe to events")

		print("Ready to go!")


	def onFaceDetected(self, *_args):
		global vct
		""" When a face is detected, NAO will start talking 
		"""
		# Unsubscribe to the event when talking to avoid repetitions
		memory.unsubscribeToEvent("FaceDetected", "StartUp")

		global config
		config = {"bodyLanguageMode":"contextual"} # set body language to contextual
		asr.say(vct + "Hello, my name is Mario!", config) # say hello
		print("Hello, my name is Mario!")
		time.sleep(1)

		# Subscribe to the WordRecognized event and to SpeechRecognition
		speech.subscribe("speechTest")
		memory.subscribeToEvent("WordRecognized", "StartUp", "initWordRecognised")
		# Unsubscribe from SpeechRecognition
		speech.unsubscribe("speechTest")
        

	def initWordRecognised(self, key, value, message):
		global playerNum, config, wordRecog, vct
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		#wordRecog = value[0]
		wordRecog = "<...> hello <...>"
		print wordRecog
		#if (len(wordRecog) > 1):
		if wordRecog == "<...> hello <...>" or wordRecog == "<...> Mario <...>" :
			asr.say(vct + "How many people are playing dominoes with me today? \\pau=1000\\ Please state either \\pau=500\\ one \\pau=500\\ or \\pau=500\\ three.", config)
			print("How many people are playing dominoes with me today?")
			time.sleep(1)            
			speech.subscribe("speechTest")
			memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognised")
			speech.unsubscribe("speechTest")
		else:
			print("Hello?")
			#self.getName()
			speech.subscribe("speechTest")
			memory.subscribeToEvent("WordRecognized", self.getName(), "initWordRecognised")
			speech.unsubscribe("speechTest")
            
	def onWordRecognised(self, key, value, message):
		global playerNum, config, wordRecog, vct
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		#wordRecog = value[0]
		wordRecog = "<...> one <...>"
		print wordRecog
		if wordRecog == "<...> one <...>" or wordRecog == "<...> three <...>":
			asr.say(vct + "Great!", config)
			print("Great!")
			#time.sleep(1)
			asr.say(vct + "Please may you deal the tiles?", config)
			print("Please may you deal the tiles?")
			tracker.stopTracker()
			#posture.goToPosture("Crouch", 0.5)
			if wordRecog == "<...> one <...>":
				playerNum = 1
				mainDomino.main()
            	
                #return playerNum
			elif wordRecog == "<...> three <...>":
				playerNum = 3
				mainDomino.main()
                #return playerNum
		else:
			#asr.say("Pardon?", config)
			print(vct + "Pardon?")
			speech.subscribe("speechTest")
			memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognised")
			speech.unsubscribe("speechTest")
        #return wordRecog, value
        

	def yesNoRecognised(self, key, value, message):
		global gameTable, wordRecog, config, vct
		gameTable = []
		# print initDomino.double
		# targetName = "Face"
		# tracker.track(targetName)
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
        #wordRecog = "<...> yes <...>"
		print value
		d1 = np.zeros((1,2)) # first tile to be played in the game
		if wordRecog == "<...> no <...>":   
			if initDomino.double == []: # if player doesnt have a double AND robot doesnt, then ask about pips
				asr.say(vct + "The highest sum of pips on one tile is " + str(initDomino.maxi), config)
				time.sleep(2)
				asr.say(vct + "Who will start?", config)
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "firstPlayerRecognised")
				speech.unsubscribe("speechTest")
			elif len(initDomino.double) >= 1: # if player doesnt have a double AND robot does, then robot goes first
				asr.say(vct + "OK", config)
				time.sleep(1)
				asr.say(vct + "I will start", config)
				initDomino.robotStart()

		elif wordRecog == "<...> yes <...>":
			if initDomino.double == []:# if player does have a double AND robot doesn't, player goes first
			# asr.say("I do not have a double", config)
			# time.sleep(2)
				asr.say(vct + "You can go first", config)
				initDomino.playerStart(1)
			#mainDomino.InitGame()

			elif len(initDomino.double) >= 1: # if player does have a double AND robot does, then compare
				asr.say(vct + "Who has the highest double?")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "firstPlayerRecognised")
				speech.unsubscribe("speechTest")

		# Wait for the player to say 'you' or 'i' or 'Mario' will start ##
		else:
			asr.say(vct + "Sorry?", config)
			time.sleep(1)
			speech.subscribe("speechTest")           
			memory.subscribeToEvent("WordRecognized", self.getName(), "yesNoRecognised")   
			speech.unsubscribe("speechTest")  

	def firstPlayerRecognised(self, key, value, message):
		global playerNum, config, wordRecog, start, vct
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
		print wordRecog
		if mainDomino.playerNum == 1:
			if wordRecog == "<...> you <...>":
				asr.say(vct + "Great!", config)
				time.sleep(1)
				asr.say(vct + "I will start", config)
				start = 0
				initDomino.robotStart()

			elif wordRecog == "<...> I <...>" or wordRecog == "<...> me <...>":
				asr.say(vct + "Cool!", config)
				time.sleep(1)
				asr.say(vct + "You start", config)
				start = 1
				initDomino.playerStart(start)
			else:
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "firstPlayerRecognised")
				speech.unsubscribe("speechTest")
				#mainDomino.InitGame()

		elif mainDomino.playerNum == 3:
			if wordRecog == "<...> you <...>" or wordRecog == "<...> Mario <...>":
				asr.say(vct + "Great!", config)
				time.sleep(1)
				asr.say(vct + "I will start", config)
				start = 0
				initDomino.robotStart()
				
			if wordRecog == "<...> one <...>":
				asr.say(vct + "Lovely!", config)
				time.sleep(1)
				asr.say(vct + "Player one starts", config)
				start = 1

			if wordRecog == "<...> two <...>":
				asr.say(vct + "Nice!", config)
				time.sleep(1)
				asr.say(vct + "Player two starts", config)
				start = 2

			if wordRecog == "<...> three <...>":
				asr.say(vct + "Ace!", config)
				time.sleep(1)
				asr.say(vct + "Player three starts", config)
				start = 3
			initDomino.playerStart(start)
				#mainDomino.InitGame()
		else:
			asr.say(vct + "Pardon?", config)
			speech.subscribe("firstPlayerRecognised")
			memory.subscribeToEvent("WordRecognized", self.getName(), "firstPlayerRecognised")
			speech.unsubscribe("firstPlayerRecognised")

        #return wordRecog, value, start
    
	def passRecognised(self, key, value, message):
		global playerNum, config, wordRecog, player1Play, vct
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
		print wordRecog
		#if (len(wordRecog) > 1):
		if wordRecog == "<...> pass <...>":
			asr.say(vct + "OK", config)
			#print("How many people are playing dominoes with me today?")
			time.sleep(1)
			mainDomino.playerPass()
			playerPlay = "pass"  
			#return      
			# else:
			#     print("You want to pass?")
			#     speech.subscribe("speechTest")
			#     memory.subscribeToEvent("WordRecognized", self.getName(), "passRecognised")
			#     speech.unsubscribe("speechTest")


# Function to recognise what the player has played, by the player verbally telling NAO.
	def domPlayedRecognised(self, key, value, message):
		global config, wordRecog, competitive, player1Play
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
		print wordRecog
		if wordRecog == "<...> pass <...>":
			mainDomino.playerPass()
		if wordRecog == "<...> zero <...>":
			# go to recognise next number
			player1Play = [0]
		elif wordRecog == "<...> one <...>":
			# go to recognise next number
			player1Play = [1]
		elif wordRecog == "<...> two <...>":
			# go to recognise next number
			player1Play = [2]
		elif wordRecog == "<...> three <...>":
			# go to recognise next number
			player1Play = [3]
		elif wordRecog == "<...> four <...>":
			# go to recognise next number
			player1Play = [4]
		elif wordRecog == "<...> five <...>":
			# go to recognise next number
			player1Play = [5]
		elif wordRecog == "<...> six <...>":
			# go to recognise next number
			player1Play = [6]		
		else:
			if competitive:
				asr.say("What?", config)
			else:
				asr.say("Pardon?", config)
			speech.subscribe("speechTest")
			memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised")
			speech.unsubscribe("speechTest")
		speech.subscribe("speechTest")
		memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
		speech.unsubscribe("speechTest")
		print("player1Play"); print player1Play


	def domPlayedRecognised1(self, key, value, message):
		global config, wordRecog, competitive, player1Play
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
		print wordRecog
		if player1Play[0] == 0:
			if wordRecog == "<...> zero <...>":
				asr.say("zero, zero?", config)
				time.sleep(1)
				mainDomino.zeroZero()
			elif wordRecog == "<...> one <...>":
				asr.say("zero, one?", config)
				time.sleep(1)
				mainDomino.zeroOne()
			elif wordRecog == "<...> two <...>":
				asr.say("zero, two?", config)
				time.sleep(1)
				mainDomino.zeroTwo()
			elif wordRecog == "<...> three <...>":
				asr.say("zero, three?", config)
				time.sleep(1)
				mainDomino.zeroThree()
			elif wordRecog == "<...> four <...>":
				asr.say("zero, four?", config)
				time.sleep(1)
				mainDomino.zeroFour()
			elif wordRecog == "<...> five <...>":
				asr.say("zero, five?", config)
				time.sleep(1)
				mainDomino.zeroSix()
			elif wordRecog == "<...> six <...>":
				asr.say("zero, six?", config)
				time.sleep(1)
				player1Play = [0, 6]
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 1:
			if wordRecog == "<...> zero <...>":
				asr.say("one, zero?", config)
				time.sleep(1)
				mainDomino.zeroOne()
			elif wordRecog == "<...> one <...>":
				asr.say("one, one?", config)
				time.sleep(1)
				mainDomino.oneOne()
			elif wordRecog == "<...> two <...>":
				asr.say("one, two?", config)
				time.sleep(1)
				mainDomino.oneTwo()
			elif wordRecog == "<...> three <...>":
				asr.say("one, three?", config)
				time.sleep(1)
				mainDomino.oneThree()
			elif wordRecog == "<...> four <...>":
				asr.say("one, four?", config)
				time.sleep(1)
				mainDomino.oneFour()
			elif wordRecog == "<...> five <...>":
				asr.say("one, five?", config)
				time.sleep(1)
				mainDomino.oneFive()
			elif wordRecog == "<...> six <...>":
				asr.say("one, six?", config)
				time.sleep(1)
				mainDomino.oneSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 2:
			if wordRecog == "<...> zero <...>":
				asr.say("two, zero?", config)
				time.sleep(1)
				mainDomino.zeroTwo()
			elif wordRecog == "<...> one <...>":
				asr.say("two, one?", config)
				time.sleep(1)
				mainDomino.oneTwo()
			elif wordRecog == "<...> two <...>":
				asr.say("two, two?", config)
				time.sleep(1)
				mainDomino.twoTwo()
			elif wordRecog == "<...> three <...>":
				asr.say("two, three?", config)
				time.sleep(1)
				mainDomino.twoThree()
			elif wordRecog == "<...> four <...>":
				asr.say("two, four?", config)
				time.sleep(1)
				mainDomino.twoFour()
			elif wordRecog == "<...> five <...>":
				asr.say("two, five?", config)
				time.sleep(1)
				mainDomino.twoFive()
			elif wordRecog == "<...> six <...>":
				asr.say("two, six?", config)
				time.sleep(1)
				mainDomino.twoSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 3:
			if wordRecog == "<...> zero <...>":
				asr.say("three, zero?", config)
				time.sleep(1)
				mainDomino.zeroThree()
			elif wordRecog == "<...> one <...>":
				asr.say("three, one?", config)
				time.sleep(1)
				mainDomino.oneThree()
			elif wordRecog == "<...> two <...>":
				asr.say("three, two?", config)
				time.sleep(1)
				mainDomino.twoThree()
			elif wordRecog == "<...> three <...>":
				asr.say("three, three?", config)
				time.sleep(1)
				mainDomino.threeThree()
			elif wordRecog == "<...> four <...>":
				asr.say("three, four?", config)
				time.sleep(1)
				mainDomino.threeFour()
			elif wordRecog == "<...> five <...>":
				asr.say("three, five?", config)
				time.sleep(1)
				mainDomino.threeFive()
			elif wordRecog == "<...> six <...>":
				asr.say("three, six?", config)
				time.sleep(1)
				mainDomino.threeSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 4:
			if wordRecog == "<...> zero <...>":
				asr.say("four, zero?", config)
				time.sleep(1)
				mainDomino.zeroFour()
			elif wordRecog == "<...> one <...>":
				asr.say("four, one?", config)
				time.sleep(1)
				mainDomino.oneFour()
			elif wordRecog == "<...> two <...>":
				asr.say("four, two?", config)
				time.sleep(1)
				mainDomino.twoFour()
			elif wordRecog == "<...> three <...>":
				asr.say("four, three?", config)
				time.sleep(1)
				mainDomino.threeFour()
			elif wordRecog == "<...> four <...>":
				asr.say("four, four?", config)
				time.sleep(1)
				mainDomino.fourFour()
			elif wordRecog == "<...> five <...>":
				asr.say("four, five?", config)
				time.sleep(1)
				mainDomino.fourFive()
			elif wordRecog == "<...> six <...>":
				asr.say("four, six?", config)
				time.sleep(1)
				mainDomino.fourSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 5:
			if wordRecog == "<...> zero <...>":
				asr.say("five, zero?", config)
				time.sleep(1)
				mainDomino.zeroFive()
			elif wordRecog == "<...> one <...>":
				asr.say("five, one?", config)
				time.sleep(1)
				mainDomino.oneFive()
			elif wordRecog == "<...> two <...>":
				asr.say("five, two?", config)
				time.sleep(1)
				mainDomino.twoFive()
			elif wordRecog == "<...> three <...>":
				asr.say("five, three?", config)
				time.sleep(1)
				mainDomino.threeFive()
			elif wordRecog == "<...> four <...>":
				asr.say("five, four?", config)
				time.sleep(1)
				mainDomino.fourFive()
			elif wordRecog == "<...> five <...>":
				asr.say("five, five?", config)
				time.sleep(1)
				mainDomino.fiveFive()
			elif wordRecog == "<...> six <...>":
				asr.say("five, six?", config)
				time.sleep(1)
				mainDomino.fiveSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		elif player1Play[0] == 6:
			if wordRecog == "<...> zero <...>":
				asr.say("six, zero?", config)
				time.sleep(1)
				mainDomino.zeroSix()
			elif wordRecog == "<...> one <...>":
				asr.say("six, one?", config)
				time.sleep(1)
				mainDomino.oneSix()
			elif wordRecog == "<...> two <...>":
				asr.say("six, two?", config)
				time.sleep(1)
				mainDomino.twoSix()
			elif wordRecog == "<...> three <...>":
				asr.say("six, three?", config)
				time.sleep(1)
				mainDomino.threeSix()
			elif wordRecog == "<...> four <...>":
				asr.say("six, four?", config)
				time.sleep(1)
				mainDomino.fourSix()
			elif wordRecog == "<...> five <...>":
				asr.say("six, five?", config)
				time.sleep(1)
				mainDomino.fiveSix()
			elif wordRecog == "<...> six <...>":
				asr.say("six, six?", config)
				time.sleep(1)
				mainDomino.sixSix()
			else:
				asr.say("Please can you repeat the second number you just said")
				speech.subscribe("speechTest")
				memory.subscribeToEvent("WordRecognized", self.getName(), "domPlayedRecognised1")
				speech.unsubscribe("speechTest")
		

	def correctIncorrectRecognised(self, key, value, message):
		global playerNum, config, wordRecog, start, player1Play, gameTable
		print("Word recognised:") # print out what nao heard
		memory.unsubscribeToEvent("WordRecognized", self.getName()) # stop listening
		wordRecog = value[0]
		print wordRecog
		if wordRecog == "<...> no <...>":
			asr.say("Can you show me the tile?", config)
			mainDomino.showTile()
		elif wordRecog == "<...> yes <...>":
			playersInput.carryOn()
		else:
			asr.say("Sorry?")
			speech.subscribe("speechTest")
			memory.subscribeToEvent("WordRecognized", self.getName(), "correctIncorrectRecognised")
			speech.unsubscribe("speechTest")


def main():
	global competitive, StartUp, gameTable, player1Play
	""" Main entry point
	"""
	# Broker to communicate with NAO
	#phrases.competitive("begin")
	phrases.supportive("begin")
	myBroker = ALBroker("myBroker",
	   "0.0.0.0",   # listen to anyone
	   0,           # find a free port and use it
	   "Mario.local",         # parent broker IP
	   9559)       # parent broker port

	global StartUp, playerNum
	StartUp = StartUpModule("StartUp")

	competitive = True # or False for the socialness of nao


	try:
		while True:
			time.sleep(1)

			# if playerNum == 1:
			# 	mainDomino.one()
			# elif playerNum == 3:
			# 	mainDomino.four()
			# #elif start == 0:

			# elif start != 0 and start != None:
			#     mainDomino.playerStart(1)

			#elif start == 2:

			#elif start == 3:

	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
		motion.rest()
		myBroker.shutdown()
		sys.exit(0)



if __name__ == "__main__":

	main()
