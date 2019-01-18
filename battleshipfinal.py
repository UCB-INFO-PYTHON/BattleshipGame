## Battleship Game in Python by Steve Dille
## 11/13/18

class Colors:
	""" Class used for color printing of letters 
	"""
	blue = '\033[94m'
	endc = '\033[0m'
	bold = '\033[1m'
	red ='\033[31m'
	green='\033[32m'


class Battleship_board:
    """ This class makes the board object. There are 3 board instances in the game: 
    	player, computer and player shot view (which shows the computer's board with only 
    	the player's shots marked Hit or Miss. Boards are a list of lists 10x10 initially 
    	set to all "O" to look like holes in the actual game"
    """ 
    def __init__(self, board = []):
        
        self.board = board
        self.board = [[]]*10
        
        i=0
        for i in range (10):
            self.board [i] = ['O','O','O','O','O','O','O','O','O','O']
        return
    

class Ship:
    """Class ship is an object that has the 5 ships for the player and computer.  
    Ship_names for each object will contain the remaining ships left. Ships dictionary has
    the size which is eventualy decremented by the shot optimizer. 
    """
    
    row_number = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}
    def __init__(self, ships={}, ship_names={}):       
        ships = {"A":5,"B":4,"S":3,"C":3,"D":2}
        ship_names = {"A":"Aircraft Carrier", "B":"Battleship", "S":"Submarine", 
                      "C":"Cruiser", "D":"Destroyer"}
        self.ships = ships
        self.ship_names = ship_names
        return

    def input_number(self, message):
        """ This method is used to validate and accept integer input. Returns an integer.
        """
        while True:
            try:
                userInput = int(input(message))       
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                return userInput 
                break 


    def print_board(self, board_type, board):
        """ Function to print boards in the game. Accepts the board_type (player,computer) 
        which is used in the title and the board to print
        """
        self.board_type = board_type
        self.board = board
        row_letter = ["A","B","C","D","E","F","G","H","I","J"]
        
        print("                 ", self.board_type , "Board")
        print()
        print (Colors.bold + "     1    2    3    4    5    6    7    8    9   10")
        print (Colors.endc, end='')
        
        # Blue for ocean holes and bold black for ships, green for misses, red for hits.  
        i = 0
        for x in self.board:
            print(Colors.bold + row_letter[i], end='    ')
            print (Colors.endc, end='')
            for y in x:
                if y =="O":
                    print(Colors.blue + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                elif y =="H":
                    print(Colors.red + Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                elif y =="M":
                    print(Colors.green + Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                else:
                    print (Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
            i +=1
            print()
        print()
        return
    
    
    def no_other_ship_test (self, board, x, y, direction, size):
        """ Function used in ship placement to validate the player or computer random 
            number generator do not place ships on top of each other. Accepts a board, 
            x,y coordinates, direction (horizontal or vertical) and size. Returns True if 
            there is no other ship overlapping this proposed placement or False otherwise.
        """
        self.board = board
        self.x = x
        self.y = y
        self.direction = direction
        self.size = size
        
        if self.direction == "H":
            for i in range (0, self.size):
                if self.board [self.y][self.x+i] != "O":
                    return False
        else:
            for i in range (0, self.size):
                if self.board [self.y+i][self.x] != "O":
                    return False
        return True           

    
    def place_ships_player (self, board, ships):
        """ This function accepts the player board object instance and the set of ships 
        	and allows the player to place the ships in valid locations.
        """
        self.board = board
        self.ships = ships
        ships_left = ["A", "B", "C", "D", "S"]
        rows = ["A","B","C","D","E","F","G","H","I","J"]
        
        # place ships until all 5 are placed
        while len(ships_left) >0:
            print ("Enter the ship you wish to place - (D)estoyer, (C}ruiser, (S)ubmarine, (B)attleship, (A)ircraft Carrier")
            print ("Ship sizes: Destroyer(2), Cruiser(3), Submarine(3), Battleship(4), Aircraft Carrier(5). Do not to exceed board size.")
            print ("You still need to place ", ships_left)
            while True:
                ship_type = input ("Enter single letter for ship type ").upper()
                if ship_type in ships_left:
                    break
            print()
            print ("Ships are placed horizontally left to right or vertically top to bottom starting with your coordinates(row,col).")
            while True:
                row_letter = input ("Enter row letter (A-J) ").upper()
                if row_letter in rows:
                    break
            y = Ship.row_number[row_letter]
            while True:
                x = self.input_number("Enter column number (1-10) ") 
                if x >= 1 and x <= 10:
                    x -=1
                    break
            while True:
                direction = input ("Enter Orientation 'H' for horizontal or 'V' for vertical ").upper()
                if direction == "H" or direction == "V":
                    break
            print()
            
			# Check for out of bounds on the board
            if (
                (direction == "H" and x + self.ships[ship_type] > 10) 
                or (direction == "V" and y + self.ships[ship_type] > 10)
            ):
                print ("Ship placement will extend beyond board boundaries. Please retry.")
                print()
                continue

			# Check for valid placement using no other ship test
            if direction == "H":
                # if placing a ship on top of one, return control to while
                if self.no_other_ship_test (self.board, x, y, direction, self.ships[ship_type]) == False:
                        print ("You may not place one ship on top of another ship.  Try again")
                        continue
                # place letters representing the ship on the board, remove the ship from 
                # the list to be placed         
                for i in range (0,self.ships[ship_type]):
                    self.board [y][x+i] = ship_type
                ships_left.remove(ship_type)   
                if len(ships_left) >0:
                    print("Here is your Player Board so far.")
                    self.print_board("Player", self.board)
                print()
                time.sleep(1)
            else:
                if direction == "V":
                    # if placing a ship on top of one, return control to while
                    if self.no_other_ship_test (self.board, x, y, direction, self.ships[ship_type]) == False:
                        print ("You may not place one ship on top of another ship.  Try again")
                        continue
                    # place letters representing the ship on the board, remove the ship 
                    # from the list to be placed       
                    for i in range (0,self.ships[ship_type]):
                        self.board [y+i][x] = ship_type
                    ships_left.remove(ship_type)   
                    if len(ships_left) >0:
                        print("Here is your Player Board so far.")
                        self.print_board("Player", self.board)
                    print()
                    time.sleep(1)
        time.sleep(1)    
        return
        
    def place_ships_computer (self, board, ships):
        """ This function accepts the computer board object instance and the set of ships 
            and using random numbers, places the ships in valid locations.
        """
        self.board = board
        self.ships = ships
        
        # generate random coordinates and ensure board position is valid
        for ship in self.ships:
            valid = False
            while (not valid):
                valid = True
                x = random.randint(0,9)
                y = random.randint(0,9)
                o = random.randint(0,1)
                if o == 0: 
                    direction = "V"
                else:
                    direction = "H"
                # if placing a ship on top of one, return control to while
                if direction == "H" and (x + self.ships[ship] <= 10):
                    if self.no_other_ship_test (self.board, x, y, direction, self.ships[ship]) == False:
                        valid = False
                        continue
                    # place letters representing the ship on the board, remove the ship 
                    # from the list to be placed       
                    for i in range (0,self.ships[ship]):
                        self.board [y][x+i] = ship
                # if H and the ship is actually off the board (failed if above), return 
                # control to the while loop
                elif direction == "H":
                    valid = False
                    continue
                else:
                	# if the orientation is vertical and ship not off the board vertically 
                	# keep processing
                    if (y + self.ships[ship] <= 10):
                        if self.no_other_ship_test (self.board, x, y, direction, self.ships[ship]) == False:
                            valid = False
                            continue
                        # place letters representing the ship on the board, remove the 
                        # ship from the list to be placed       
                        for i in range (0,self.ships[ship]):
                            self.board [y+i][x] = ship
                    else:
                        # if not H or V and a valid pacement, return control to the while 
                        # to generate new coordinates
                        valid = False
                        continue
        return


class Play_Game:  
    """This class plays the game.  It accepts the player and computer board, ships and ship names and player shots
    """     
     
    last_shot = "miss"
    shoot_list = []
    rows = ["A","B","C","D","E","F","G","H","I","J"]

    def __init__(self, p1_board, p1_ships, p1_ships_names, c1_board, c1_ships, c1_ships_names, p1_shots):
        """play the game while turn is = computer or player and stop when it is set to end.
        """
        self.p1_board = p1_board
        self.p1_ships = p1_ships
        self.p1_ships_names = p1_ships_names
        self.c1_board = c1_board
        self.c1_ships = c1_ships
        self.c1_ships_names = c1_ships_names
        self.p1_shots = p1_shots
        
        turn = 'player'
        while turn != "end":
            turn = self.take_turns(turn)
            continue      
        return

    def input_number(self, message):
        """ This method is used to validate and accept integer input.  
        It returns an integer.
        """
        while True:
            try:
                userInput = int(input(message))       
            except ValueError:
                print("Not an integer! Try again.")
                contin
            else:
                return userInput 
                break 

    def print_board(self, board_type, board):
        """ Function to print boards in the game. Accepts the board_type (player,computer) 
        which is used in the title and the board to print
        """
        self.board_type = board_type
        self.board = board
        row_letter = ["A","B","C","D","E","F","G","H","I","J"]
        
        print("                 ", self.board_type , "Board")
        print()
        print (Colors.bold + "     1    2    3    4    5    6    7    8    9   10")
        print (Colors.endc, end='')
        
        # Blue for ocean holes and bold black for ships, green for misses, red for hits.  
        i = 0
        for x in self.board:
            print(Colors.bold + row_letter[i], end='    ')
            print (Colors.endc, end='')
            for y in x:
                if y =="O":
                    print(Colors.blue + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                elif y =="H":
                    print(Colors.red + Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                elif y =="M":
                    print(Colors.green + Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
                else:
                    print (Colors.bold + '{0:<5}'.format(y), end='')
                    print (Colors.endc, end='')
            i +=1
            print()
        print()
        return
        
    def take_turns (self, turn):
        """ This method accepts the turn as player or computer and calls the appropriate 
            function and alterntes turns.  It returns the turn reset to player,computer or
            if game tracker determines the game is over, it will set turn to end.  
        """
        if turn == "player":
            self.player_shot ()
            turn = "computer"
            time.sleep(1)
        else:
            self.computer_shot()
            turn = "player"
            time.sleep(1)
                                                                                          
        if self.game_tracker() == 0:
            return turn
        elif self.game_tracker() == 1:
            print ("Player has lost.")
        else:
            print ("Player has won.")
        return "end"    

    def optimize_shot (self, ship_type, x, y):
        """ This method accepts ship type and coordinates if a hit occurs by the computer.
            This simulates a user honing in to finish off a ship. This will create the
            list of subsequent shots for the computer instead of resorting to random shots
            and not fully sinking a ship. The shoot_list is used by computer_shot instead
            of random shots until it is empty. To average out some misses a missed
            shot is placed in the list
        """
        self.ship_type = ship_type
        self.x = x
        self.y = y
        
        # place correct shots in the shoot_list and set vertical or horizontal
        for i in range (0,10):
            if self.p1_board [self.y][i] == self.ship_type and i != self.x:
                self.shoot_list.append ([self.y,i])
                horizontal = True    
        for i in range (0,10):
            if self.p1_board [i][self.x] == self.ship_type and i != self.y:
                self.shoot_list.append ([i,self.x])
                horizontal = False

        # Add in a shot to be missed as a player on average would not always guess right
        if horizontal:
            if self.y + 1 < 10:
                if self.p1_board [self.y + 1][self.x] == "O":
                    self.shoot_list.append ([self.y + 1, self.x])
            else: 
                if self.y - 1 >= 0:   
                    if self.p1_board [self.y - 1][self.x] == "O":
                        self.shoot_list.append ([self.y - 1, self.x])
         
        if not horizontal:
            if self.x + 1 < 10:
                if self.p1_board [self.y][self.x + 1] == "O":
                    self.shoot_list.append ([self.y, self.x + 1])
            else: 
                if self.x - 1 >= 0:   
                    if self.p1_board [self.y][self.x - 1] == "O":
                        self.shoot_list.append ([self.y, self.x - 1])         
        return   

    def player_shot (self):       
        """ Method to accept coordinate input and process player shots. Prints the player
            shot view and theor ship board too.
        """
        print("")
        time.sleep(1)
        self.print_board("Player Ship", self.p1_board)
        time.sleep(1)
        self.print_board("Player Shot View", self.p1_shots)

        # Accept coordinates from the player
        while True:
            print ("Player, take your shot by entering a row and column coordiate pair")          
            while True:
                row_letter = input ("Enter row letter (A-J) ").upper()
                if row_letter in self.rows:
                    break
            y = Ship.row_number[row_letter]
            while True:
                x = self.input_number("Enter column number (1-10) ") 
                if x >= 1 and x <= 10:
                    x -=1
                    break                    
            # Stop the player from making repeat shots where they already missed or hit
            if self.repeat_location(self.c1_board, y, x) == False:
                break
            else:
                print ('')
                print ("You already shot at that location.  Try again")

        # Show hits or misses until the ship has been sunk, then print the name of ship 
        # and remaining ships to be sunk. Update the player shot view and computer board.        
        if self.hit_miss(self.c1_board, y, x) == "hit":
            print ("Hit! at", row_letter, x+1)
            last_ship_hit = self.c1_board[y][x]
            self.c1_ships[last_ship_hit] -= 1 
            if self.c1_ships[last_ship_hit] == 0: 
                print (self.c1_ships_names[last_ship_hit], "was sunk")
                del self.c1_ships_names[last_ship_hit]     
                if len(self.c1_ships_names) > 0:
                    print ("Remaining ships", self.c1_ships_names)
                else:
                    print()
            self.c1_board[y][x] = "H"
            self.p1_shots[y][x] = "H"
        else:
            print ("Miss at", row_letter, x+1)
            self.c1_board[y][x] = "M"
            self.p1_shots[y][x] = "M"
        return
    
    def computer_shot (self):
        """ Method to use coordinates generated and process computer shots.
        """ 
        row_list = ["A","B","C","D","E","F","G","H","I","J"]
        print("")
        print ("Computer is shooting")     

        # Process coordinates from the optimzed shoot_list or generate random ones
        if self.last_shot == "hit" and len(self.shoot_list) > 0:
            t = self.shoot_list.pop()
            y = t[0]
            x = t[1]
        else:  
            while True:
                x = random.randint(0,9)
                y = random.randint(0,9)
                if self.repeat_location(self.p1_board, y, x) == False:
                    break 
                    
        # Let an optimize_shot generated miss on purpose and just pass through 
        if self.hit_miss(self.p1_board, y, x) == "miss" and len(self.shoot_list) > 0:
            print ("Miss by computer at", row_list[y], x+1)
            self.p1_board[y][x] = "M"
            return        
        
        if self.hit_miss(self.p1_board, y, x) == "hit":
            last_ship_hit = self.p1_board[y][x]

            # if last_shot == "miss" call optimizer function to create the list of next 
            # shots by looking at player p1.board
            if self.last_shot == "miss":
                self.optimize_shot(last_ship_hit, x, y)
            print ("Hit by computer! at", row_list[y], x+1)
            self.last_shot = "hit"

            # decrement the ship size counter until you know it was sunk
            self.p1_ships[last_ship_hit] -= 1 
            if self.p1_ships[last_ship_hit] == 0: 
                print (self.p1_ships_names[last_ship_hit], " was sunk")
                self.last_shot = "miss"
                del self.p1_ships_names[last_ship_hit]     # remove item from dictionary
            self.p1_board[y][x] = "H"
        else:
            print ("Miss by computer at", row_list[y], x+1)
            self.last_shot = "miss"
            self.p1_board[y][x] = "M"
        time.sleep(1)
        return

    
    def hit_miss (self, board, y, x):
        """ Accepts a board and a pair of coordinates and returns "hit" or "miss"
        """
        self.board = board
        self.y = y
        self.x = x
        if self.board[self.y][self.x] == "O" or self.board[self.y][self.x] == "M" :
            return "miss"
        else:
            return "hit"
    
    def game_tracker (self):
        """ Determines if all player ships are sunk and returns 1, all computer ships are
            sunk and returns 2 or if game is still on and returns 0
        """
        if len(self.p1_ships_names) == 0:
            return 1
        elif len (self.c1_ships_names) == 0:
            return 2
        return 0

    def repeat_location (self, board, y, x):
        """ Accepts a board and an x,y coordinate pair.  Returns True if the shot was at
            a location already shot into or False otherwise
        """
        self.board = board
        self.y = y
        self.x = x
        if self.board[self.y][self.x] == "M" or self.board[self.y][self.x] == "H":
            return True
        else:
            return False

class Game_Engine:  
    """This class creates new instances of the game objects and loops"""      

    def __init__(self):
        #Generate new object instances and play the game until the player selects play again = "N"
        while True:
            # Generate player and computer boards and a view for the player of shots only
            
            p1 = Battleship_board()
            p1_shot_view = Battleship_board()
            c1 = Battleship_board()

            # Generate player and computer ships
            p_ships = Ship()
            c_ships = Ship()

            print()
            print("Let's play Battleship against the computer.  You will set up your ships in secret and so will the computer.")
            print("Then you will take turns firing at each others ships. The computer will keep track of the hits and misses for you.")
            print("You can see your ship status on the Player Board and track where you have fired on the Player Shot View Board.")
            print("First let's set up your five ships.")
            time.sleep(7)
            print()

            # Place the ships by player and computer
            p_ships.place_ships_player(p1.board, p_ships.ships)
            c_ships.place_ships_computer(c1.board, c_ships.ships)

            print()
            print("Let's play now. You can shoot first. I'll keep you appraised on the Player Shot View Board.")
            print()
            play_again = "Y"
            Play_Game(p1.board, p_ships.ships, p_ships.ship_names, c1.board, c_ships.ships, c_ships.ship_names, p1_shot_view.board)
            while True:
                play_again = input ("Play again? Enter (Y) for Yes or (N) for No").upper()
                if play_again == "Y" or play_again == "N":
                    break
            if play_again == "N":
                    break


        
# Main Battleship Program - Steve Dille
# The main program simply starts the game engine object which plays the game.

import random
import os
import time

Game_Engine()




## Test Code Tools Area

#To Initialize Player Board to avoid having to place the 5 ships

##p1.board [1] = ['O','D','D','O','O','O','O','O','O','O']  # just for testing to avoid having to input player
##p1.board [3] = ['O','O','O','O','A','A','A','A','A','O']
##p1.board [5] = ['S','S','S','O','O','O','O','O','O','O']
##p1.board [7] = ['O','B','B','B','B','O','O','O','O','O']
##p1.board [9] = ['O','O','O','O','O','O','O','C','C','C']
##c1.print_board("Computer Ship")
