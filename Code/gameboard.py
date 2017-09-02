#Lewis Mazzei - Fusion/Code/gameboard.py
#Note: If a comment is not on the same line then the corresponding comment to a line or chunk of code will be above it

#import 'random' package
import random 
#import tile class
from tile import Tile

class Gameboard():
	#constructor
	def __init__(self, username, state = [['Empty' for col in range(5)] for row in range(5)], level = 1, tiles = [], score = 0):
		self.state = state #set the 'state' attribute
		self.level = level #set the 'level' attribute
		self.tiles = tiles #set the 'tiles' attribute
		self.score = score #set the 'score' attribute
		self.username = username #set the 'username' attribute
		#map the level number to the lowest tile that can spawn
		self.levelDict = {1:1, 2:12, 3:23, 4:34, 5:45, 6:56, 7:67, 8:78, 9:89, 10:100, 11:111} 

	def spawn(self):
		gameOver = False #first assume that the game is not over
		element = random.randint(self.levelDict[self.level], self.levelDict[self.level] + 1) #find lowest tiles for level and pick one randomly

		emptyCells = [] #initialise a list that will store the locations of all the empty cells within the game board
		row = 0 #initialise a row variable
		col = 0 #initialise a column variable

		#generate a list of locations of empty cells inside the gameboard
		[[emptyCells.append((row, col)) for col in range(5) if self.state[row][col] == 'Empty'] for row in range(5)]
		
		try: 
			location = random.choice(emptyCells) #try to pick one of these cells at random...
		except IndexError: #...unless there's no more cells to pick from i.e. the board is full...
			gameOver = True #...then flag this fact...
			return gameOver #...and return it

		#use random element and location to create a new tile
		newTile = Tile(element, location)
		#update list of tile objects
		self.tiles.append(newTile)
		#update game state
		self.state[location[0]][location[1]] = newTile

	def tilesLeft(self):
		#sort the tiles array so it loops through in the opposite direction that they are moving...
		#...this is so that multiple layers of tiles can all move without being incorrectly blocked...
		#...by tiles that are still to move themselves
		self.leftSort()
		tile = 0 #start with first tile
		tileHasMoved = False #first assumes that no tiles will move
		combinedTiles = [] #keeps track of which tiles have already been part of a combination to avoid double combinations in one key press
		while tile < len(self.tiles): #loop through all tiles on the board
			shift = 0 #reset shift for new tile
			combinationOccured = False #first assumes that no combination will occur 
			tileAlreadyCombined = False #first assumes that the tile has not been combined yet this key press
			while True: #keep checking until another tile is found (i.e. obstruction) or the edge of the grid is reached
				col = self.tiles[tile].location[1] - (shift + 1) #potential new column for the tile, this column will be checked to see...
				if col >= 0: #...if it actually exists...
					cell = self.state[self.tiles[tile].location[0]][col] #...it does so we'll take a look at this cell and check...
					if type(cell) == Tile: #...if it is occupied by a tile...
						if self.tiles[tile].element == cell.element: #...and whether that tile is an identical element...
							#...if this is the case then...
							for combinedtile in combinedTiles: #take a look at the combined tiles list...
								if cell == combinedtile: #...and if the current cell contains a tile that has been combined...
									tileAlreadyCombined = True #...then flag this fact
							if tileAlreadyCombined == False: #only combine if the tile has not already been combined this key press
								#...combine the current tile with the cell we are looking at (and append it to the combined tiles list)...
								combinedTiles.append(self.combine(self.tiles[tile], cell)) 
								tileHasMoved = True #there has been movement so flag this fact
								combinationOccured = True #there has been combination so flag this fact
							break #...and break out the while loop on the same tile index as the current tile will now be removed from the tiles list
						else: #...or if the tiles are different elements...
							break #...then break out the loop and update as that tile's path is tileed, it cannot move further along
					#...or if the contents are 'empty'...
					else: #...then is it...
						if col == 0: #...an edge? if so then...
							shift += 1 #...increase the shift (as the cell we are looking at is actually (shift + 1)), break and update
							break
						else: #...a non-edge? if so then...
							shift += 1 #...increase the shift and go to the top of the while loop
				else:
					break #...if it doesn't exist then it's hit the edge so break out loop and update the state with the current shift

			if combinationOccured == False: #if combination has occured then the combine function updates the state appropriately
				#set the tiles current location to 'empty'
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = 'Empty'
				#update tile's location to the furthest possible cell along (in the direction that the tile is travelling)
				self.tiles[tile].location = (self.tiles[tile].location[0], self.tiles[tile].location[1] - shift)
				#update gameboard's state to show this change in location 
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = self.tiles[tile]
				
				if shift != 0: #if there has been any movement then then flag this fact...
					tileHasMoved = True

				tile += 1 #we now return to the top of the while loop so move onto next tile
		
		return tileHasMoved #...so that we know whether to spawn another tile or not

	def tilesRight(self):
		#sort the tiles array so it loops through in the opposite direction that they are moving...
		#...this is so that multiple layers of tiles can all move without being incorrectly tileed...
		#...by tiles that are still to move themselves
		self.rightSort() 
		tile = 0 #start with first tile
		tileHasMoved = False #first assumes that no tiles will move
		combinedTiles = [] #keeps track of which tiles have already been part of a combination to avoid double combinations in one key press
		while tile < len(self.tiles): #loop through all tiles on the board
			shift = 0 #reset shift for new tile
			combinationOccured = False #first assumes that no combination will occur 
			tileAlreadyCombined = False #first assumes that the tile has not been combined yet this key press
			while True: #keep checking until another tile is found (i.e. obstruction) or the edge of the grid is reached
				col = self.tiles[tile].location[1] + (shift + 1) #potential new column for the tile, this column will be checked to see...
				if col <= 4: #...if it actually exists...
					cell = self.state[self.tiles[tile].location[0]][col] #...it does so we'll take a look at this cell and check...
					if type(cell) == Tile: #...if it is occupied by a tile...
						if self.tiles[tile].element == cell.element: #...and whether that tile is an identical element...
							#...if this is the case then...
							for combinedtile in combinedTiles: #take a look at the combined tiles list...
								if cell == combinedtile: #...and if the current cell contains a tile that has been combined...
									tileAlreadyCombined = True #...then flag this fact
							if tileAlreadyCombined == False: #only combine if the tile has not already been combined this key press
								#...combine the current tile with the cell we are looking at (and append it to the combined tiles list)...
								combinedTiles.append(self.combine(self.tiles[tile], cell))
								tileHasMoved = True #there has been movement so flag this fact
								combinationOccured = True #there has been combination so flag this fact
							break #...and break out the while loop on the same tile index as the current tile will now be removed from the tiles list
						else: #...or if the tiles are different elements...
							break #...then break out the loop and update as that tile's path is tileed, it cannot move further along
					#...or if the contents are 'empty'...
					else: #...then is it...
						if col == 4: #...an edge? if so then...
							shift += 1 #...increase the shift (as the cell we are looking at is actually (shift + 1)), break and update
							break
						else: #...a non-edge? if so then...
							shift += 1 #...increase the shift and go to the top of the while loop
				else:
					break #...if it doesn't exist then it's hit the edge so break out loop and update the state with the current shift

			if combinationOccured == False: #if combination has occured then the combine function updates the state appropriately
				#set the tiles current location to 'empty'
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = 'Empty'
				#update tile's location to the furthest possible cell along (in the direction that the tile is travelling)
				self.tiles[tile].location = (self.tiles[tile].location[0], self.tiles[tile].location[1] + shift)
				#update gameboard's state to show this change in location 
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = self.tiles[tile]
				
				if shift != 0: #if there has been any movement then then flag this fact...
					tileHasMoved = True

				tile += 1 #we now return to the top of the while loop so move onto next tile
		
		return tileHasMoved #...so that we know whether to spawn another tile or not

	def tilesUp(self):
		#sort the tiles array so it loops through in the opposite direction that they are moving...
		#...this is so that multiple layers of tiles can all move without being incorrectly tileed...
		#...by tiles that are still to move themselves
		self.upSort() 
		tile = 0 #start with first tile
		tileHasMoved = False #first assumes that no tiles will move
		combinedTiles = [] #keeps track of which tiles have already been part of a combination to avoid double combinations in one key press
		while tile < len(self.tiles): #loop through all tiles on the board
			shift = 0 #reset shift for new tile
			combinationOccured = False #first assumes that no combination will occur 
			tileAlreadyCombined = False #first assumes that the tile has not been combined yet this key press
			while True: #keep checking until another tile is found (i.e. obstruction) or the edge of the grid is reached
				row = self.tiles[tile].location[0] - (shift + 1) #potential new column for the tile, this column will be checked to see...
				if row >= 0: #...if it actually exists...
					cell = self.state[row][self.tiles[tile].location[1]] #...it does so we'll take a look at this cell and check...
					if type(cell) == Tile: #...if it is occupied by a tile...
						if self.tiles[tile].element == cell.element: #...and whether that tile is an identical element...
							#...if this is the case then...
							for combinedtile in combinedTiles: #take a look at the combined tiles list...
								if cell == combinedtile: #...and if the current cell contains a tile that has been combined...
									tileAlreadyCombined = True #...then flag this fact
							if tileAlreadyCombined == False: #only combine if the tile has not already been combined this key press
								#...combine the current tile with the cell we are looking at (and append it to the combined tiles list)...
								combinedTiles.append(self.combine(self.tiles[tile], cell)) 
								tileHasMoved = True #there has been movement so flag this fact
								combinationOccured = True #there has been combination so flag this fact
							break #...and break out the while loop on the same tile index as the current tile will now be removed from the tiles list
						else: #...or if the tiles are different elements...
							break #...then break out the loop and update as that tile's path is tileed, it cannot move further along
					#...or if the contents are 'empty'...
					else: #...then is it...
						if row == 0: #...an edge? if so then...
							shift += 1 #...increase the shift (as the cell we are looking at is actually (shift + 1)), break and update
							break
						else: #...a non-edge? if so then...
							shift += 1 #...increase the shift and go to the top of the while loop
				else:
					break #...if it doesn't exist then it's hit the edge so break out loop and update the state with the current shift

			if combinationOccured == False: #if combination has occured then the combine function updates the state appropriately
				#set the tiles current location to 'empty'
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = 'Empty'
				#update tile's location to the furthest possible cell along (in the direction that the tile is travelling)
				self.tiles[tile].location = (self.tiles[tile].location[0] - shift, self.tiles[tile].location[1])
				#update gameboard's state to show this change in location 
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = self.tiles[tile]
				
				if shift != 0: #if there has been any movement then then flag this fact...
					tileHasMoved = True

				tile += 1 #we now return to the top of the while loop so move onto next tile
		
		return tileHasMoved #...so that we know whether to spawn another tile or not
	
	def tilesDown(self):
		#sort the tiles array so it loops through in the opposite direction that they are moving...
		#...this is so that multiple layers of tiles can all move without being incorrectly tileed...
		#...by tiles that are still to move themselves
		self.downSort() 
		tile = 0 #start with first tile
		tileHasMoved = False #first assumes that no tiles will move
		combinedTiles = [] #keeps track of which tiles have already been part of a combination to avoid double combinations in one key press
		while tile < len(self.tiles): #loop through all tiles on the board
			shift = 0 #reset shift for new tile
			combinationOccured = False #first assumes that no combination will occur 
			tileAlreadyCombined = False #first assumes that the tile has not been combined yet this key press
			while True: #keep checking until another tile is found (i.e. obstruction) or the edge of the grid is reached
				row = self.tiles[tile].location[0] + (shift + 1) #potential new column for the tile, this column will be checked to see...
				if row <= 4: #...if it actually exists...
					cell = self.state[row][self.tiles[tile].location[1]] #...it does so we'll take a look at this cell and check...
					if type(cell) == Tile: #...if it is occupied by a tile...
						if self.tiles[tile].element == cell.element: #...and whether that tile is an identical element...
							#...if this is the case then...
							for combinedtile in combinedTiles: #take a look at the combined tiles list...
								if cell == combinedtile: #...and if the current cell contains a tile that has been combined...
									tileAlreadyCombined = True #...then flag this fact
							if tileAlreadyCombined == False: #only combine if the tile has not already been combined this key press
								#...combine the current tile with the cell we are looking at (and append it to the combined tiles list)...
								combinedTiles.append(self.combine(self.tiles[tile], cell)) 
								tileHasMoved = True #there has been movement so flag this fact
								combinationOccured = True #there has been combination so flag this fact
							break #...and break out the while loop on the same tile index as the current tile will now be removed from the tiles list
						else: #...or if the tiles are different elements...
							break #...then break out the loop and update as that tile's path is tileed, it cannot move further along
					#...or if the contents are 'empty'...
					else: #...then is it...
						if row == 4: #...an edge? if so then...
							shift += 1 #...increase the shift (as the cell we are looking at is actually (shift + 1)), break and update
							break
						else: #...a non-edge? if so then...
							shift += 1 #...increase the shift and go to the top of the while loop
				else:
					break #...if it doesn't exist then it's hit the edge so break out loop and update the state with the current shift

			if combinationOccured == False: #if combination has occured then the combine function updates the state appropriately
				#set the tiles current location to 'empty'
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = 'Empty'
				#update tile's location to the furthest possible cell along (in the direction that the tile is travelling)
				self.tiles[tile].location = (self.tiles[tile].location[0] + shift, self.tiles[tile].location[1])
				#update gameboard's state to show this change in location 
				self.state[self.tiles[tile].location[0]][self.tiles[tile].location[1]] = self.tiles[tile]
				
				if shift != 0: #if there has been any movement then then flag this fact...
					tileHasMoved = True

				tile += 1 #we now return to the top of the while loop so move onto next tile
		
		return tileHasMoved #...so that we know whether to spawn another tile or not

	def combine(self, tile, otherTile):
		newElement = tile.element + 1 #increment the element
		self.tiles.remove(tile) #remove the moving tile from list of tiles
		otherTileIndex = self.tiles.index(otherTile) #get the index of the tile that is going to be 'hit' (the non-moving one)
		self.tiles[otherTileIndex].element = newElement #update the non-moving tile's element
		self.state[tile.location[0]][tile.location[1]] = 'Empty' #update the location of where the moving tile started moving to 'empty'
		self.score += (tile.element * 2)
		return otherTile

	def leftSort(self):
		#clear current list of tiles, the list will be made to contain all tiles in order... 
		#...from the left and top most to the right and bottom most cell
		del self.tiles[:]
		
		for col in range(5): #scans column by column from the right to the left...
			for row in range(5): #...scanning down each row in that column from top to bottom...
				cell = self.state[row][col] #current cell
				if type(cell) == Tile: #... and if the current cell is a tile...
					self.tiles.append(cell) #...then append the tile back to the list

	def rightSort(self):
		#clear current list of tiles, the list will be made to contain all tiles in order... 
		#...from the right and top most to the left and bottom most cell
		del self.tiles[:]
		
		for col in range(4, -1, -1): #scans column by column from the left to the right...
			for row in range(5): #...scanning down each row in that column from top to bottom
				cell = self.state[row][col] #current cell
				if type(cell) == Tile: #... and if the current cell is a tile...
					self.tiles.append(cell) #...then append the tile back to the list

	def upSort(self):
		#clear current list of tiles, the list will be made to contain all tiles in order... 
		#...from the top and left most to the bottom and right most cell
		del self.tiles[:]
		
		for row in range(5): #scans row by row from the top to the bottom...
			for col in range(5): #...scanning across each column in that row from left to right
				cell = self.state[row][col] #current cell
				if type(cell) == Tile: #... and if the current cell is a tile...
					self.tiles.append(cell) #...then append the tile back to the list

	def downSort(self):
		#clear current list of tiles, the list will be made to contain all tiles in order... 
		#...from the bottom and left most to the top and right most cell
		del self.tiles[:]
		
		for row in range(4, -1, -1): #scans row by row from the bottom to the top...
			for col in range(5): #...scanning across each column in that row from left to right
				cell = self.state[row][col] #current cell
				if type(cell) == Tile: #... and if the current cell is a tile...
					self.tiles.append(cell) #...then append the tile back to the lis