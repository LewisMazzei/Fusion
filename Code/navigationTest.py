def mainMenuLoop():
	while True:
		print('Main Menu')
		command = input('Input: ')
		if command == 'new game':
			nameInputLoop()
		elif command == 'load game':
			nameInputLoop()
		elif command == 'leaderboard':
			leaderboardLoop()
		elif command == 'instructions':
			instructionsLoop()

def nameInputLoop():
	while True:
		print('Name Input')
		command = input('Input: ')
		if command == 'name entered':
			gameLoop()
		elif command == 'back':
			return

def gameLoop():
	while True:
		print('Game')
		command = input('Input: ')
		if command == 'options':
			optionsLoop()
		elif command == 'game over':
			mainMenuLoop()

def optionsLoop():
	while True:
		print('Options')
		command = input('Input: ')
		if command == 'leaderboard':
			leaderboardLoop()
		elif command == 'main menu':
			mainMenuLoop()
		elif command == 'continue':
			return
		elif command == 'instructions':
			instructionsLoop()

def leaderboardLoop():
	while True:
		print('Leaderboard')
		command = input('Input: ')
		if command == 'back':
			return

def instructionsLoop():
	while True:
		print('Instructions')
		command = input('Input: ')
		if command == 'back':
			return

mainMenuLoop()