#Lewis Mazzei - Fusion/Code/main.py
#Note: If a comment is not on the same line then the corresponding comment to a line or chunk of code will be above it

#import relevant packages 
import pygame, random, time, os, pickle, re
#import gameboard class
from gameboard import Gameboard 
#import tile class
from tile import Tile
#setup file: includes all functions needed for setting up pygame window and some constant variables needed throughout the process of running the game
from setup import DISPLAY_WIDTH, DISPLAY_HEIGHT, display, clock, BLACK, WHITE, gridDictCoords, gridDictDimensions, elementSymbols
#drawing file: includes all functions required to draw the different screens and their elements 
from drawing import font, createTextObjects, drawButton, drawLabel, drawInputBox, drawGameScreenHeader, drawGameBoard, drawTiles, drawGameScreen, drawMainMenuScreen, drawInstructionsScreen, drawNameInputScreen, drawLeaderboardGrid, drawLeaderboardContents, drawLeaderboardScreen, drawOptionsScreen
#loops file: includes all files required to listen for event triggers and is what calls the relevant draw functions when the screen is to be changed
from loops import gameLoop, mainMenuLoop, instructionsLoop, nameInputLoop, leaderboardLoop, optionsLoop, usernameSubmitted, bubbleSort, saveGameState, openGameSave, deleteGameSave, initSpawn, updateLeaderboard

#starts the user on the main menu when they first run the game
mainMenuLoop()