#Lewis Mazzei - Fusion/Code/drawing.py
#Note: If a comment is not on the same line then the corresponding comment to a line or chunk of code will be above it

#import relevant packages
import pygame, pickle
#colours file: stores colour values for each tile value
from colours import tileColours
#setup file: includes all functions needed for setting up pygame window and some constant variables needed throughout the process of running the game
from setup import DISPLAY_WIDTH, DISPLAY_HEIGHT, display, clock, BLACK, WHITE, gridDictCoords, gridDictDimensions, elementSymbols

#used for establishing font sizes (and boldness) for text elementSymbols throughout the game, both fonts are part of a folder containing several 'ubuntu' style fonts
def font(size, bold = True): 
	if bold:
		font = pygame.font.Font('/home/lewis/Documents/School/Fusion/External Files/ubuntu-font-family/Ubuntu-M.ttf', size) #ubuntu-M: bold font
	else:
		font = pygame.font.Font('/home/lewis/Documents/School/Fusion/External Files/ubuntu-font-family/Ubuntu-R.ttf', size) #ubuntu-R: thinner non-bold font

	return font

#used for defining text's surface and the area around it
def createTextObjects(text, font, colour): 
	try:
		textSurf = font.render(text, True, colour) #creates a surface for the text to sit on...
	except TypeError: #the render function only takes in Unicode or bytecode, an empty string does not count as this and will through a typeError if this occurs
		textSurf = font.render(None, True, colour) #in this case just pass in 'null' which is an acceptable value
	return textSurf, textSurf.get_rect() #returns the surface and a rectangle that surrounds that surface

#used for drawing button elementSymbols
def drawButton(outlineColour, outlineCoords, outlineWeight, text, font, textColour):
	#create box for button
	buttonRect = pygame.draw.rect(display, outlineColour, outlineCoords, outlineWeight)
	#create the text surface and it's respective rectangle for positioning
	buttonTextSurf, buttonTextRect = createTextObjects(text, font, textColour)
	#position text in the center of the button's box using the text surface's corresponding rectangle
	buttonTextRect.center = ((outlineCoords[0] + (outlineCoords[2] / 2)), (outlineCoords[1] + (outlineCoords[3] / 2)))
	#draw button to display
	display.blit(buttonTextSurf, buttonTextRect)
	
	return buttonRect #returns the properties of the rectangle so that they can be referred to 

#used for drawing label elementSymbols
def drawLabel(text, font, colour, coords):
	#create the text surface and it's respective rectangle for positioning
	labelTextSurf, labelTextRect = createTextObjects(text, font, colour)
	#position the label using the text surface's corresponding rectangle
	labelTextRect.center = coords
	#draw button to display
	display.blit(labelTextSurf, labelTextRect)

	return labelTextRect #returns the properties of the rectangle so that they can be referred to 

#used for drawing input box elementSymbols (very similiar to a button but text is dynamic) 
def drawInputBox(outlineColour, outlineCoords, outlineWeight, font, textColour, text = ''):
	#create box for input box
	inputBoxRect = pygame.draw.rect(display, outlineColour, outlineCoords, outlineWeight)
	#create the text surface and it's respective rectangle for positioning
	inputBoxTextSurf, inputBoxTextRect = createTextObjects(text, font, textColour)
	#position text in the center of the input box using the text surface's corresponding rectangle
	inputBoxTextRect.center = ((outlineCoords[0] + (outlineCoords[2] / 2)), (outlineCoords[1] + (outlineCoords[3] / 2)))
	#draw input box to display
	display.blit(inputBoxTextSurf, inputBoxTextRect)
	
	return inputBoxRect #returns the properties of the rectangle so that they can be referred to

#used for drawing the header elements on the game screen
def drawGameScreenHeader(username, level, score, highscore):
	featureList = [drawLabel(username, font(25), BLACK, (100, 40)), #draw 'Username' label
				   drawLabel(level, font(30), BLACK, ((DISPLAY_WIDTH / 2), 60)), #draw 'Level Number' label
				   drawLabel(score, font(25), BLACK, (400, 40)), #draw 'Score' label
				   drawLabel(highscore, font(25), BLACK, (400, 90)), #draw 'Highscore' label
				   drawButton(BLACK, [50, 70, 120, 40], 3, 'Options', font(25), BLACK)] #draw 'Options' button

	return featureList #returns the properties of the various elements on this screen to the loop function so that things such as button clicks can be listened for

#used for drawing the game board grid on the game screen
def drawGameBoard():
	pygame.draw.rect(display, BLACK, [50, 150, 400, 400], 5) #draw the grid square
	for yCoord in range(230, 550, 80):
		pygame.draw.line(display, BLACK, (50, yCoord), (450, yCoord), 3) #draw the horizontal grid lines
	for xCoord in range(130, 450, 80):
		pygame.draw.line(display, BLACK, (xCoord, 150), (xCoord, 550), 3) #draw the vertical grid lines
	
#used for drawing the tiles onto the game board grid
def drawTiles(gameboard):
	for tile in gameboard.tiles: #for each tileon the board...
		location = gridDictCoords[tile.location] #...find the centre of the cell which it needs to be drawn onto...
		colour = tileColours[gameboard.level - 1][(tile.element - 1) % 11] #...and select the appropriate colour for tile

		startX = gridDictCoords[tile.location][0] - 37 #set the x...
		startY = gridDictCoords[tile.location][1] - 37 #...and y coordinate for the top left pixel of the tile
		width = gridDictDimensions[tile.location][0] #set the width...
		height = gridDictDimensions[tile.location][1] #...and height for the tile, depending on where the tile has to be drawn this will change due to the thickness of grid lines around it

		tileRect = pygame.draw.rect(display, colour, [startX, startY, width, height]) #draw the tile rectangle 
		drawLabel(str(elementSymbols[tile.element - 1]), font(25), BLACK, (gridDictCoords[tile.location][0], gridDictCoords[tile.location][1] - 15)) #draw the element name onto the tile
		drawLabel(str(tile.element), font(25), BLACK, (gridDictCoords[tile.location][0], gridDictCoords[tile.location][1] + 20)) #draw the element number onto the tile

#used for drawing the elements that make up the game screen whilst the 'gameLoop' is running
def drawGameScreen(gameboard):
	display.fill(WHITE) #wipe screen before updating pixels
	with open('/home/lewis/Documents/School/Fusion/External Files/Leaderboard.pickle', 'rb') as file: #open leaderboard file
		try: 
			namesAndScores = pickle.load(file) #get names and scores from 'leaderboard' file...
			highScore = namesAndScores[-1][1] #...and get the highscore from the list of names and scores
		except EOFError: #unless the file is empty...
			highScore = 0 #...in which case just set the highscore to 0
		features = drawGameScreenHeader(gameboard.username, 'LVL {}'.format(str(gameboard.level)), 'Score: {}'.format(str(gameboard.score)), 'Hi-Score: {}'.format(highScore)) #draw the header 
	drawGameBoard() #draw the board
	drawTiles(gameboard) #draw the tiles

	return features #return properties of all elements

#used for drawing the elements that make up the main menu screen whilst the 'mainMenuLoop' is running
def drawMainMenuScreen():
	display.fill(WHITE) #wipe screen before updating pixels

	drawLabel('Fusion', font(140, True), (178, 34, 34), (DISPLAY_WIDTH / 2, 150)) #draw title screen header

	featureList = [drawButton(BLACK, [125, 320, 250, 50], 3, 'New Game', font(25), BLACK), #draw 'New Game' button
				   drawButton(BLACK, [125, 380, 250, 50], 3, 'Load Game', font(25), BLACK), #draw 'Load Game' button
				   drawButton(BLACK, [125, 440, 250, 50], 3, 'Leaderboard', font(25), BLACK), #draw 'Leaderboard' button
				   drawButton(BLACK, [125, 500, 250, 50], 3, 'Instructions', font(25), BLACK)] #draw 'Instructions' button

	return featureList #return properties of all elements

#used for drawing the elements that make up the instructions screen whilst the 'instructionsLoop' is running
def drawInstructionsScreen():
	display.fill(WHITE) #wipe screen before updating pixels

	img = pygame.image.load('/home/lewis/Documents/School/Fusion/External Files/Instructions Screen.png')

	display.blit(img, (35,0))

	featureList = [drawButton(BLACK, [360, 5, 130, 35], 3, 'BACK', font(25), BLACK)]

	return featureList #return properties of all elements

#used for drawing the elements that make up the name input screen whilst the 'nameInputLoop' is running
def drawNameInputScreen(newGame, username):
	display.fill(WHITE) #wipe the display before updating pixels

	#the only element that changes when drawing this screen is the text on the button used to submit the username and proceed to the game 
	if newGame:
		featureList = [drawLabel('Please enter a username between 3 and', font(25), BLACK, (250, 235)), #draw prompt text
					   drawLabel('8 characters long', font(25), BLACK, (250, 270)), #draw prompt text
					   drawInputBox(BLACK, [150, 310, 200, 30], 2, font(25), BLACK, username), #draw input box
					   drawButton(BLACK, [150, 365, 200, 30], 3, 'Start Game', font(25), BLACK), #draw 'Start Game' button
					   drawButton(BLACK, [320, 35, 130, 35], 3, 'BACK', font(25), BLACK)] #draw 'Back' button
	else:
		featureList = [drawLabel('Please enter the username from your', font(25), BLACK, (250, 235)), #draw prompt text
					   drawLabel('previous game.', font(25), BLACK, (250, 270)), #draw prompt text
					   drawInputBox(BLACK, [150, 310, 200, 30], 2, font(25), BLACK, username), #draw input box
					   drawButton(BLACK, [150, 365, 200, 30], 3, 'Continue Game', font(25), BLACK), #draw 'Continue Game' button
					   drawButton(BLACK, [320, 35, 130, 35], 3, 'BACK', font(25), BLACK)] #draw 'Back' button

	return featureList #return properties of all elements

#draws the leaderboard grid that the leaderboard contents will populate
def drawLeaderboardGrid():
	pygame.draw.rect(display, BLACK, [50, 90, 400, 475], 5) #draw rectangle that leaderboard gird will be drawn in
	
	for yCoord in range(565, 90, -43):
		pygame.draw.line(display, BLACK, (50, yCoord), (450, yCoord), 3) #draw horizontal grid lines
	pygame.draw.line(display, BLACK, (90, 90), (90, 565), 3) #draw the vertical line seperating the 'numbers' column and the 'username' column
	pygame.draw.line(display, BLACK, (270, 90), (270, 565), 3) #draw the vertical line seperating the 'username' column and the 'score' column

#draws the contents that fill the leaderboard grid
def drawLeaderboardContents():
	drawLabel('Username', font(25), BLACK, (175, 110)) #draw the column header for the 'username' column
	drawLabel('Score', font(25), BLACK, (355, 110)) #draw the column header for the 'score' column

	numCol = ['#', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] #the hash will be the column header for the 'numbers' column with the numbers themselves populating the rows of the column
	row = 1 #start at the first row
	for yCoord in range(110, 545, 43):
		drawLabel(numCol[row - 1], font(25), BLACK, (70, yCoord)) #for each row draw the corresponding number in the correct place on the grid
		row += 1 #incrememnt row

	with open('/home/lewis/Documents/School/Fusion/External Files/Leaderboard.pickle', 'rb') as file: #open the 'leaderboard' file
		try: 
			namesAndScores = pickle.load(file) #load up the scores...
			namesAndScores.reverse() #... and reverse the list so that the highest score is the first element
		except EOFError: #unless there are no scores in the file...
			namesAndScores = [] #...in which case, the list is just empty
	entry = 0
	for yCoord in range(153, 545, 43): #for each row...
		if entry < len(namesAndScores): #...if there is still place on the table...
			drawLabel(namesAndScores[entry][0], font(25, False), BLACK, (175, yCoord)) #...then draw the appropriate username onto the appropriate row and column...
			drawLabel(str(namesAndScores[entry][1]), font(25, False), BLACK, (355, yCoord)) #...and the appropriate score onto the appropriate row and column
			entry += 1 #increment entry number

#used for drawing the elements that make up the instructions screen whilst the 'leaderboardLoop' is running
def drawLeaderboardScreen():
	display.fill(WHITE) #wipe screen before updating pixels

	drawLeaderboardGrid() #draw the leaderboard grid

	featureList = [drawLabel('Leaderboard', font(40), BLACK, (155, 50)), #draw the leaderboard header 
				   drawButton(BLACK, [320, 35, 130, 35], 3, 'BACK', font(25), BLACK)] #draw the 'back' button

	drawLeaderboardContents() #draw the contents of the leaderboard into the leaderboard grid

	return featureList #return properties of all elements

#used for drawing the elements that make up the options screen whilst the 'optionsLoop' is running
def drawOptionsScreen():
	display.fill(WHITE) #wipe screen before updating pixels

	featureList = [drawLabel('Options', font(60), BLACK, (DISPLAY_WIDTH / 2, 85)), #draw the options header
				   drawButton(BLACK, [160, 230, 190, 60], 3, 'LEADERBOARD', font(25), BLACK), #draw the 'leaderboard' button
				   drawButton(BLACK, [160, 330, 190, 60], 3, 'MAIN MENU', font(25), BLACK), #draw the 'main menu' button
				   drawButton(BLACK, [160, 430, 190, 60], 3, 'CONTINUE', font(25), BLACK)] #draw the 'continue' button

	return featureList #return properties of all elements