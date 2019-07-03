import sys
from naoqi import ALProxy
import random
import initDomino
import time


def competitive(state):
	global asr, leds, vct
	leds = ALProxy("ALLeds", "Mario.local", 9559)
	leds.fadeRGB('AllLeds', 1, 0, 0,1)
	if state == "begin":
		vct = "\\vct=75\\"

	if state == "deal":
	# To say when dealing the cards
		deal = [vct + "I am here to win!", \
		vct + "I am going to win.", \
		vct + "I can not wait to win."]
		say = random.choice(deal)
		initDomino.asr.say(say)
	elif state == "playersTurn":
	# To say during other peoples turn
		playersTurn = [vct + "I am better at this than you", \
		vct + "You obviously haven't played Dominoes in a while.", \
		vct + "Are you sure you want to play that tile?", \
		vct + "Hmmm, \\pau=1000\\ I would not have played that tile then.", \
		vct + "Smells like cheating in here"]
		say = random.choice(playersTurn)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "robotsTurn":	
	# To say when it is NAO's turn
		robotsTurn = [vct + "My turn!",\
		vct + "Let me show you how it's done",\
		vct + "YES!", \
		vct + "I know!"]
		say = random.choice(robotsTurn)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "robotWins":
		# To say if NAO wins
		robotWins = [vct + "It was fun beating you", \
		vct + "No one can beat me!!"]
		say = random.choice(robotWins)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "playerWins":
		# To say if player wins
		playerWins = [vct + "I obviously was not playing properly", \
		vct + "I don't want to play anymore"]
		say = random.choice(playerWins)
		initDomino.asr.say(say)
		time.sleep(3)


def supportive(state):
	global asr, leds, vct
	leds = ALProxy("ALLeds", "Mario.local", 9559)
	leds.fadeRGB('AllLeds', 0, 1, 0,1)
	if state == "begin":
		vct = "\\vct=100\\"

	if state == "deal":
	# To say when dealing the cards
		deal = [vct + "I cannot wait to play with you!", \
		vct + "Let's have some fun!"]
		say = random.choice(deal)
		initDomino.asr.say(say)
	elif state == "playersTurn":
	# To say during other peoples turn
		playersTurn = [vct + "That was a good move", \
		vct + "Nice!", \
		vct + "That's great!", \
		vct + "You are good at this game!"]
		say = random.choice(playersTurn)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "robotsTurn":	
	# To say when it is NAO's turn
		robotsTurn = [vct + "Hm",\
		vct + "Let me think",\
		vct + "YES!", \
		vct + "I know!"]
		say = random.choice(robotsTurn)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "robotWins":
		# To say if NAO wins
		robotWins = [vct + "That's ok, maybe you will win next time", \
		vct + "That was such a fun game"]
		say = random.choice(robotWins)
		initDomino.asr.say(say)
		time.sleep(3)
	elif state == "playerWins":
		# To say if player wins
		playerWins = [vct + "Wow, you are a pro!", \
		vct + "I would love to play with you again"]
		say = random.choice(playerWins)
		initDomino.asr.say(say)
		time.sleep(3)

	# tts.say("\\vct=25\\ bbbbbbbbuuuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrppppppppppppppppppppp \\pau=1000\\ woops, sorry!")
