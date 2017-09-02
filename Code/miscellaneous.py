#Lewis Mazzei - Fusion/Code/miscellaneous.py
#Note: If a comment is not on the same line then the corresponding comment to a line or chunk of code will be above it
import pygame, pickle, os
from gameboard import Gameboard
from setup import DISPLAY_WIDTH, DISPLAY_HEIGHT, display, clock, BLACK, WHITE, gridDictCoords, gridDictDimensions, elementNameDict, elements
from drawing import font, createTextObjects, drawButton, drawLabel, drawInputBox, drawGameScreenHeader, drawGameBoard, drawTiles, drawGameScreen, drawMainMenuScreen, drawInstructionsScreen, drawNameInputScreen, drawLeaderboardGrid, drawLeaderboardContents, drawLeaderboardScreen, drawOptionsScreen
from loops import gameLoop, mainMenuLoop, instructionsLoop, nameInputLoop, leaderboardLoop, optionsLoop

def bubbleSort(lst):
	sorted = False #first assume that list is not sorted

	while not sorted: #keep making passes until list is sorted
		sorted = True #assume that the list is sorted...
		for i in range(len(lst) - 1): #for every element in the list...
			if lst[i][1] > lst[i + 1][1]: #...check if the next element is greater than it
				sorted = False #...until a swap is carried out
				lst[i], lst[i + 1] = lst[i + 1], lst[i] #swap the elements

def saveGameState(gameboard):
	with open('/home/lewis/Documents/School/Computing Project/External Files/Game Saves/{}.pickle'.format(gameboard.username), 'wb') as file:
		pickle.dump([gameboard.username, gameboard.state, gameboard.level, gameboard.tiles, gameboard.score], file)

def openGameSave(username):
	with open('/home/lewis/Documents/School/Computing Project/External Files/Game Saves/{}.pickle'.format(username), 'rb') as file:
		username, state, level, tiles, score = pickle.load(file)
		return Gameboard(username, state, level, tiles, score)

def deleteGameSave(username):
	os.remove('/home/lewis/Documents/School/Computing Project/External Files/Game Saves/{}.pickle'.format(username))

def initSpawn(gameboard):
	if random.randint(0, 1) == 0: #create a 50/50 chance that...
		if gameboard.spawn() == True: #...one tile will be spawned, and if that tile causes the grid to overflow then...
			updateLeaderboard(gameboard) #...update the leaderboard with the user's score (if it makes the top 10)...
			deleteGameSave(gameboard.username)
			leaderboardLoop(gameOver = True) #...and then switch to the leaderboard screen
	else: #...or...
		if gameboard.spawn() == True: #...two tiles will be spawned 
			updateLeaderboard(gameboard)
			deleteGameSave(gameboard.username)
			leaderboardLoop(gameOver = True) #(or if the board is full then it will go finish the game)
		elif gameboard.spawn() == True:
			updateLeaderboard(gameboard)
			deleteGameSave(gameboard.username)
			leaderboardLoop(gameOver = True) #(or if the board is full then it will go finish the game)

def updateLeaderboard(gameboard):
	firstNameEntered = False #assume that the list either has 0 entries or more than 1
	with open('/home/lewis/Documents/School/Computing Project/External Files/Leaderboard.pickle', 'rb') as file: #open leaderboard file
		try:
			namesAndScores = pickle.load(file) #read file and grab the current list of names and scores...
		except EOFError: #...unless there's nothing in the file, i.e. leaderboard has been wiped
			namesAndScores = [(gameboard.username, gameboard.score)] #if this is the case just set the first element of the list to the current user's name and score
			firstNameEntered = True # flag the fact that there is only one entry in the list
		if len(namesAndScores) < 10 and not firstNameEntered: #...and the list has less than more than 1 entry but less 10 entries...
			namesAndScores.append((gameboard.username, gameboard.score)) #...then just append that user's name and score to the list...
			bubbleSort(namesAndScores) #...and then put that score into place with a sort, the name and score will 'bubble' to the correct position
		elif gameboard.score > namesAndScores[0][1]: #if the current list already has 10 entries and the current score is higher than the lowest score in the list...
			namesAndScores[0] = (gameboard.username, gameboard.score) #...then replace that score... 
			bubbleSort(namesAndScores) #...and sort the list
	with open('/home/lewis/Documents/School/Computing Project/External Files/Leaderboard.pickle', 'wb') as file:
		pickle.dump(namesAndScores, file)