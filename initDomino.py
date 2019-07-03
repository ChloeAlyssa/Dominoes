import sys
import time
import numpy as np
import random
import math
import playersInput
import robotPlay
import game
import barcodeScanner
import Start
import mainDomino
import phrases
# Uncomment for robot
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBroker

#play = []
#gameTable = []
#robot = []
#playerNum = 1
#boneyard = []

dealDom = None
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


class initDominoModule():
    #def __init__(self, name):
        #ALModule.__init__(self, name)

            #################################### TESTING #################################### 
            #posture.goToPosture("Crouch", 0.5)
            

    # global speech, face, tracker, memory, motion, posture, asr, aware, play, gameTable, robot, playerNum, boneyard
    # play = []
    # gameTable = []
    # robot = []
    # playerNum = 1
    # boneyard = []
    # tracker = ALProxy("ALTracker")
    # motion = ALProxy("ALMotion")
    # asr = ALProxy("ALAnimatedSpeech")
    # speech = ALProxy("ALSpeechRecognition")
    # memory = ALProxy("ALMemory")
    # barcode = ALProxy("ALBarcodeReader")
    # barcode.subscribe("test_barcode")
    # time.sleep(10)

    # data = memory.getData("BarcodeReader/BarcodeDetected")
    # print data
    # motion.wakeUp()

    # motion.setStiffnesses("Body", 1.0)
    # config = {"bodyLanguageMode":"contextual"}

    # speech.setLanguage("English")
    # vocab = ["yes", "no"]
    # speech.setVocabulary(vocab, True)

            #playerNum = 1
            #initDominoModule.Deal()
            #dealDom.Deal()
            #################################################################################

    ################## Gets initial hand info and sets up the players hands as an empty array ##################
    def Deal(self):
        global playerNum, robot, player1, boneyard, player2, player3, cameraNo, bar, asr, motion, config, speech, memory
        global barcode, posBar
        phrases.supportive("deal")
        #phrases.competitive("deal")
        #cameraNo = 1
        init = True
        
        mainDomino.robotsTiles()
        robot = mainDomino.bar # Tiles
        posBar = mainDomino.posBar # Position of tiles

        #robot = np.array([[6, 0], [2, 3], [1, 3], [2, 4], [1, 2], [3, 5], [6, 5]])
        #robot = np.array(robot)
        print robot
        player1 = [None]*7
        #playerNum = mainDomino.playerNum
        playerNum = 1
        if playerNum == 1: # 2-player
            boneyard = [None]*14
        elif playerNum == 3: # 4-player
            player2 = [None]*7
            player3 = [None]*7
        #return robot

    ################## Checks if and what double is in the hand ##################                
    def Doubles(self):
        global d1, maxi, robot, double

        double = []
        index = 0
        # checks for doubles
        for i in range(len(robot)):
            if robot[index,0] == robot[index,1]:
                double.append(robot[index])		
            index+=1
            
            #print("Double", double)

        # if there aren't, finds the highest sum of pips
        if len(double) == 0:
            for i in range(len(robot)):
                sum1 = np.sum(robot, axis=1)
                maxi = max(sum1)
        # if there are, finds what the highest double is
        elif len(double) >= 1:
            maxi = np.amax(double)

            #return double

    ################## Decides who should go first ##################
    def FirstPlayer(self):
        global asr, config, speech, memory, double, d1, play, gameTable, playerNum, player1, maxi, start 
        global robot, player1Maxi, player2Maxi, player3Maxi, player1Double, player2Double, player3Double, start, play, wordRecog, yesNo
        global gameTable1, gameTable2, gameTable3, gameTable4, gameTable5, gameTable6, gameTable7
        start = 0
        gameTable = []

        # the player with the largest double or sum will start the game
        if playerNum == 3: # 4-player
            if double == []: # if robot doesnt have a double
                # asr.say("I do not have a double", config)
                print("i dont have a double")
            elif len(double) >= 1: # if robot does have a double
            ################## Uncomment for robot ##################
                asr.say("I have a double, it is " + str(maxi), config)
                time.sleep(1)
            asr.say("Who goes first?")
            time.sleep(1)
            ## Recognise 'one', 'two' or 'three' ##
            speech.subscribe("firstPlayerRecognised")
            time.sleep(2)
            memory.subscribeToEvent("WordRecognized", "StartUp", "firstPlayerRecognised")
            speech.unsubscribe("firstPlayerRecognised")
            Variations()
                # print("I have a double, it is " + str(maxi))
        elif playerNum == 1: # 2-player
            if double == []:
                ################## Uncomment for robot ##################
                asr.say("I do not have a double", config)
                time.sleep(2)
                # print("I don't have a double")
            else:
                ################## Uncomment for robot ##################
                asr.say("I have a double, it is " + str(maxi), config)
                time.sleep(2)
                # print("I have a double, its " + str(maxi))
            asr.say("Do you have a double?", config)
            time.sleep(1)
            speech.subscribe("speechTest")
            memory.subscribeToEvent("WordRecognized", "StartUp", "yesNoRecognised")
            speech.unsubscribe("speechTest")
            # print("Do you have a double?")
            # player1Double = raw_input("Do you have a double? (Y/N) ")
            ## Recognise "you" or "I" ##


            
            # if player1Double == "n" and double == []: # if player doesnt have a double AND robot doesnt, then ask about pips
            #     print("The highest sum of pips on one tile is " + str(maxi))
            #     player1Maxi = raw_input("What is your highest sum? ")
            #     player1Maxi = int(player1Maxi)

            #     if player1Maxi>maxi:
            #         print('You start')
            #         d1 = raw_input('*** Player 1 input tile ***')
            #         d1 = int(d1)
            #         d1 = [int(i) for i in str(d1)]

            #     else:
            #         print('I will start')
            #         start = 0
            #         d1 = random.sample(robot, 1)

            # elif player1Double == "n": # if player doesnt have a double AND robot does, then robot goes first
            #     print('I will start')
            #     start = 0
            #     d1 = random.sample(robot, 1)
                
            # elif player1Double == "y" and double == []:# if player does have a double AND robot doesn't, player goes first
            #     print('You first')
            #     d1 = raw_input('*** Player 1 input tile ***')
            #     d1 = int(d1)
            #     d1 = [int(i) for i in str(d1)]
                    
            # elif player1Double == "y" and len(double) >= 1: # if player does have a double AND robot does, then compare
            #     player1Maxi = raw_input('What is the number? ')
            #     player1Maxi = int(player1Maxi)
            #     if player1Maxi > maxi:
            #         print('You start')
            #         d1 = raw_input('*** Player 1 input tile ***')
            #         d1 = int(d1)
            #         d1 = [int(i) for i in str(d1)]

            #     else:
            #         print('I will start')
            #         start = 0
            #         d1 = random.sample(robot, 1)

            ################## Uncomment for robot ##################
            # time.sleep(1)
            ## Recognise 'yes' or 'no' ##
            # speech.subscribe("yesNo")
            #time.sleep(2)
            # memory.subscribeToEvent("WordRecognized", "StartUp", "yesNoRecognised")
            # speech.unsubscribe("yesNo")

            # start = Start.start     
            #start = 0   
            
                    
                # return d1
def playerStart(player):
    global start, gameTable, turn, player1Play, speech, memory, asr
    start = player
    asr.say("What tile are you starting with?")
    time.sleep(1)
    speech.subscribe("speechTest")
    memory.subscribeToEvent("WordRecognized", "StartUp", "domPlayedRecognised")
    speech.unsubscribe("speechTest")

def robotStart():
    global start, d1, gameTable, play, init, robot
    start = 0
    gameTable = []
    # print initDomino.d1
    d1 = random.sample(robot, 1)   

    gameTable = np.append(gameTable, d1)
    print("GameTable = ")
    print gameTable
    play = gameTable

    FirstRemove()
    # init = False
    
       
def FirstRemove():
    global maxi, player1, play, gameTable, robot, init
    if np.any(gameTable == play):
        #if np.any(gameTable == play): ######## tests
        InitMatching()
        InitRemove()
        init = False
        mainDomino.InitGame()
    else:
                # InitRemove()
        mainDomino.InitGame()
        #return robot

def InitMatching():
    global match, robot, gameTable, indx
    
    # gameTable = mainDomino.gameTable
    indx = 0
    match = []

    for i in range(len(robot)):
        if robot[indx,0] == gameTable[0] or robot[indx,0] == gameTable[-1]:
            #if np.any(robot[index,0] == gameTable):
            match = np.append(match, robot[indx])
        elif robot[indx,1] == gameTable[0] or robot[indx,1] == gameTable[-1]:
            #elif np.any(robot[index,1] == gameTable):
            match = np.append(match, robot[indx])
        indx+=1
    #return

def InitRemove():
    global player1, play, turn, robot, player2, player3, indx, asr
    # #start = 1
    # if playerNum == 3:
    #     player2 = initDomino.player2
    #     player3 = initDomino.player3



    indx = 0
    for i in range(len(robot)):
        if robot[indx,0] == play[0] and robot[indx,1] == play[1]:
                #if np.all(robot[indx] == play[0]):
            robot = np.delete(robot, [indx],0) # remove played tile from hand
            print robot
        else:				
            indx+=1
    mainDomino.pointAt()
        #return robot

    #return wordRecog, gameTable
# def Variations():
#         global player1Double, player2Double, player3Double, player1Maxi, player2Maxi, player3Maxi, play

#         if player1Double == 'n' and player2Double == 'n' and player3Double == 'n':
#                 if double == [None]:
#                         asr.say("The highest sum of pips I have on one tile is " + str(maxi), config)
#                         #player1Maxi = raw_input(name + ", what is your highest sum? ")
#                         #player1Maxi = int(player1Maxi)
#                         #print("The highest sum of pips on one tile is " + str(maxi))
#                         #player2Maxi = raw_input(name2 + ", what is your highest sum? ")
#                         #player2Maxi = int(player2Maxi)
#                         #print("The highest sum of pips on one tile is " + str(maxi))
#                         #player3Maxi = raw_input(name3 + ", what is your highest sum? ")
#                         #player3Maxi = int(player3Maxi)
#                 else:
#                         asr.say("I will start", config)
#                         start = 1
#                         d1 = random.sample(robot, 1)

#         elif player1Double == 'n' and player2Double == 'n' and player3Double == 'y':
#                 if double == [None]:
#                         print("player1 3 goes first")
#                         start = 0
#                         cameraNo = 0
#                         barcodeScanner.Scan()
#                         #play = raw_input("*** input tile ***")
#                         #play = int(play)
#                         #play = [int(i) for i in str(play)]
#                         #d1[0] = play
#                 else:
#                         player3Maxi = raw_input(name3 + ' what is the number? ')
#                         player3Maxi = int(player3Maxi)
#                         player2Maxi = -1
#                         player1Maxi = -1
#                         First4Play()


#         elif player1Double == 'n' and player2Double == 'y' and player3Double == 'n':
#                 if double == [None]:
#                         print("player1 2 goes first")
#                         start = 3
#                         play = raw_input("*** input tile ***")
#                         play = int(play)
#                         play = [int(i) for i in str(play)]
#                         d1[0] = play
#                 else:
#                         player2Maxi = raw_input(name2 + ' what is the number? ')
#                         player2Maxi = int(player2Maxi)
#                         player3Maxi = -1
#                         player1Maxi = -1
#                         First4Play()

#         elif player1Double == 'n' and player2Double == 'y' and player3Double == 'y':
#                 player2Maxi = raw_input(name2 + ' what is the number? ')
#                 player2Maxi = int(player2Maxi)
#                 player3Maxi = raw_input(name3 + ' what is the number? ')
#                 player3Maxi = int(player3Maxi)
#                 player1Maxi = -1
#                 First4Play()

#         elif player1Double == 'y' and player2Double == 'n' and player3Double == 'n':
#                 if double == [None]:
#                         print("player1 1 goes first")
#                         start = 2
#                         play = raw_input("*** input tile ***")
#                         play = int(play)
#                         play = [int(i) for i in str(play)]
#                         d1[0] = play
#                 else:
#                         player1Maxi = raw_input(name + ' what is the number? ')
#                         player1Maxi = int(player1Maxi)
#                         player2Maxi = -1
#                         player3Maxi = -1
#                         First4Play()

#         elif player1Double == 'y' and player2Double == 'n' and player3Double == 'y':
#                 player1Maxi = raw_input(name + ' what is the number? ')
#                 player1Maxi = int(player1Maxi)
#                 player3Maxi = raw_input(name3 + ' what is the number? ')
#                 player3Maxi = int(player3Maxi)
#                 player2Maxi = -1
#                 First4Play()

#         elif player1Double == 'y' and player2Double == 'y' and player3Double == 'n':
#                 player1Maxi = raw_input(name + ' what is the number? ')
#                 player1Maxi = int(player1Maxi)
#                 player2Maxi = raw_input(name2 + ' what is the number? ')
#                 player2Maxi = int(player2Maxi)
#                 player3Maxi = -1
#                 First4Play()

#         elif player1Double == 'y' and player2Double == 'y' and player3Double == 'y':
#                 if double == [None]:
#                         maxi = -1
#                 player1Maxi = raw_input(name + ' what is the number? ')
#                 player1Maxi = int(player1Maxi)
#                 player2Maxi = raw_input(name2 + ' what is the number? ')
#                 player2Maxi = int(player2Maxi)
#                 player3Maxi = raw_input(name3 + ' what is the number? ')
#                 player3Maxi = int(player3Maxi)
#                 First4Play()

#         return

# def First4Play():
#         global player1Maxi, player2Maxi, player3Maxi, maxi, d1, play, start

#         if player1Maxi>maxi and player1Maxi>player2Maxi and player1Maxi>player3Maxi:
#                 print(name + ', you first')
#                 play = raw_input("*** input tile ***")
#                 play = int(play)
#                 play = [int(i) for i in str(play)]
#                 d1[0] = play
#                 start = 0
#         elif player2Maxi>maxi and player2Maxi>player1Maxi and player2Maxi>player3Maxi:
#                 print(name2 + ', you first')
#                 play = raw_input("*** input tile ***")
#                 play = int(play)
#                 play = [int(i) for i in str(play)]
#                 d1[0] = play
#                 start = 2
#         elif player3Maxi>maxi and player3Maxi>player1Maxi and player3Maxi>player2Maxi:
#                 print(name3 + ', you first')
#                 play = raw_input("*** input tile ***")
#                 play = int(play)
#                 play = [int(i) for i in str(play)]
#                 d1[0] = play
#                 start = 3
#         else:
#                 print("I will go first")
#                 start = 1
#                 d1 = random.sample(robot, 1)

#         return


def main():
    global play, gameTable, robot, init, asr, config, speech, memory, d1, tracker, posture, leds

        # # # # # # # # # # # Uncomment for robot # # # # # # # # # # #
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, "Mario.local", 9559)
    asr = ALProxy("ALAnimatedSpeech")
    config = {"bodyLanguageMode":"contextual"}
    motion = ALProxy("ALMotion")
    speech = ALProxy("ALSpeechRecognition")
    memory = ALProxy("ALMemory")
    tracker = ALProxy("ALTracker")
    posture= ALProxy("ALRobotPosture")
    leds = ALProxy("ALLeds")
	
    global dealDom
    global init 
    init = True
    dealDom = initDominoModule()
    dealDom.Deal()
    dealDom.Doubles()
    dealDom.FirstPlayer()
    # print Start.start
    # print("and here")

    # if Start.start == None:
    #     speech.subscribe("speechTest")
    #     memory.subscribeToEvent("WordRecognized", "StartUp", "yesNoRecognised")
    #     speech.unsubscribe("speechTest")
    #     #if Start.start == 
    #     if Start.start == 0:
    #         dealDom.robotStart()
    #         dealDom.FirstRemove()
    #     elif Start.start == 1:
    #         mainDomino.playerStart(1)
    #     elif Start.start == 2:
    #         mainDomino.playerStart(2)
    #     elif Start.start == 3:
    #         mainDomino.playerStart(3)

        #if start == 0:
            #d1 = random.sample(robot, 1)
            #gameTable = np.append(gameTable, d1)
            #play = gameTable
            #dealDom.FirstRemove()
        #return robot, gameTable, init
        
    # try:
    #     while True:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         print "Interrupted by user, shutting down"
    #         motion.rest()
    #         myBroker.shutdown()
    #         sys.exit(0)

if __name__ == "__main__":
    main()
