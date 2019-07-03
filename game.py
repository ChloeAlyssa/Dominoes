import numpy as np
import initDomino
#from initDomino import gameTable
import robotPlay
import playersInput
import mainDomino
import random
import sys
import Start
import mainDomino
import phrases

# def DoublesInGame():
# 	if play[0] == play[1]:
turn = []
add = 0

def GameStatus():
    global player1, robot, turn, player2, player3, asr
    if turn[0] == 1:
        if initDomino.start != 1:
            player1 = playersInput.player1
        else:
            player1 = initDomino.player1
        if len(player1) == 0:
            initDomino.asr.say("Player 1 wins this round!!!")
            sum1 = sum(robotPlay.robot)
            addPoints(sum1)
            player1Score = score

            initDomino.asr.say("Your score is " + str(player1Score))
            phrases.supportive("playerWins")
            #phrases.competitive("playerWins")
            PlayAgain(player1Score)
        # else:
        #     if initDomino.playerNum == 1:
        #         print("ROBOTS TURN")
        #     else:
        #         print("PLAYER 2'S TURN")
                       # Turn()
    if turn[0] == 0:
        robot = robotPlay.robot
        if len(robot) == 0:
            initDomino.asr.say("I win this round!!!")
            sum1 = sum(playersInput.player1)
            addPoints(sum1)
            robotScore = score
            initDomino.asr.say("MY SCORE is " + str(robotScore))
            phrases.supportive("robotWins")
            #phrases.competitive("robotWins")
            PlayAgain(robotScore)
                        # cprint('ROBOT WINS', 'red', attrs=['blink'])
            #sys.exit()
        # else:
            # print("PLAYER 1'S TURN")	
                        # Turn()
    elif turn[0] == 2:
        player2 = playersInput.player2
        if len(player2) == 0:
            initDomino.asr.say("Player 2 wins this round!!!")
            sum1 = sum(robotPlay.robot)
            player2Score = np.sum(sum1)
            player2Score = main.Round(player2Score)
            initDomino.asr.say("YOUR SCORE is " + str(player2Score))
            phrases.supportive("playerWins")
            #phrases.competitive("playerWins")
            PlayAgain(player2Score)
        else:
            print("PLAYER 3'S TURN")
    elif turn[0] == 3:
        player3 = playersInput.player3
        if len(player1) == 0:
            initDomino.asr.say("Player 3 wins this round!!!")
            sum1 = sum(robotPlay.robot)
            player3Score = np.sum(sum1)
            player3Score = main.Round(player3Score)
            initDomino.asr.say("YOUR SCORE is " + str(player3Score))
            phrases.supportive("playerWins")
            #phrases.competitive("playerWins")
            PlayAgain(player3Score)
        else:
            print("ROBOTS TURN")
    # return

def PlayAgain(points):
        #initDomino.asr.say("Would you like to play again?")
        ###### SORT THIS OUT ######
        if points < 100:
            initDomino.asr.say("Please can you deal the tiles again?")
        else:
            initDomino.asr.say("Thanks for playing with me, \\pau=1000\\, I hope you have a lovely day!")
        # cprint('player1 WINS', 'red', attrs=['blink'])
            sys.exit()

def addPoints(sum1):

    add += np.sum(sum1)
    score = mainDomino.Round(add)
    print score
    return score

def Turn(): # Next players turn
    global turn, nextPlayer, playerNum, init

    if initDomino.playerNum == 1:
        if turn == []:
            nextPlayer = initDomino.start
            # turn = np.append(nextPlayer, turn)
        # elif turn == []:
        #     nextPlayer = initDomino.start
        elif len(turn)>=1:
            if turn[0] == 1:
                nextPlayer = 0
            elif turn[0] == 0:
                nextPlayer = 1
    elif initDomino.playerNum == 3:
        if turn == []:
            nextPlayer = mainDomino.start
            # turn = np.append(nextPlayer, turn)
        elif len(turn)>=1:
            if turn[0] == 1:
                nextPlayer = 2
            elif turn[0] == 2:
                nextPlayer = 3
            elif turn[0] == 3:
                nextPlayer = 0
            elif turn[0] == 0:
                nextPlayer = 1
    turn = np.append(nextPlayer, turn)
    # print turn
        # return turn

def GameMain():
        global gameTable, maxi, play
        # play = initDom.play
        # FirstRemove()
        Place()

