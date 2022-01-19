from os import system
from random import randint
from time import sleep
import connect_4_cpu

class ConnectGame():
    '''Class used for creating the Connect 4 grid, game and playing it'''
    
    ##Internal Methods:
    
    def __init__(self,player='X'):
        
        self.connect_grid = [[None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None]]
        
        self.player = player
        self.winner = None
        self.winning_move = [[None,None],[None,None]] #Format will be start cell(column,row) and end cell(column,row)
        self.banner = [' #########################',' # Connect 4, by Spencer #',' #########################']
        if self.player == 'X':
            self._current_turn = 'Human'
            self.opponentPiece = 'O'
        else:
            self._current_turn = 'AI'
            self.opponentPiece = 'X'
        self._piece_dict = {'X':'Human','O':'AI'}
        
    def _set_piece(self,column,piece): #Sets the piece to the top of the grid
        self.connect_grid[column][6] = piece
        
    def _eval_horizontal(self,column,row,num): #checks for 4 matching cells in a row
        c = column
        r = row
        if num == 0:
            return [True,[c,r]]
        if self.connect_grid[c+1][r] == self.connect_grid[c][r]: #checks for a horizontal match
            result = self._eval_horizontal(c+1,r,num-1) #re-runs the same method with one less 'num' looking for the next match
            return result
        return [False,0]
            
    def _eval_vertical(self,column,row,num): #checks for 4 matching cells in a row
        c = column
        r = row
        if num == 0:
            result = [True,[c,r]]
            return result
        if self.connect_grid[c][r+1] == self.connect_grid[c][r]: #checks for a vertical match
            result = self._eval_vertical(c,r+1,num-1) #re-runs the same method with one less 'num' looking for the next match
            return result
        return [False,0]
            
    def _eval_diagonal_up(self,column,row,num): #checks for 4 matching cells in a row
        c = column
        r = row
        if num == 0:
            return [True,[c,r]]
        if self.connect_grid[c+1][r+1] == self.connect_grid[c][r]: #checks for a diagonal match
            result = self._eval_diagonal_up(c+1,r+1,num-1) #re-runs the same method with one less 'num' looking for the next match
            return result
        return [False,0]

    def _eval_diagonal_down(self,column,row,num): #checks for 4 matching cells in a row
        c = column
        r = row
        if num == 0:
            return [True,[c,r]]
        if self.connect_grid[c+1][r-1] == self.connect_grid[c][r]: #checks for a diagonal match
            result = self._eval_diagonal_down(c+1,r-1,num-1) #re-runs the same method with one less 'num' looking for the next match
            return result
        return [False,0]
        
    def _eval_cell(self,column,row): #Calls upon the four sub-eval functions to evaluate if a win has occurred
        if column < 4:
            result = self._eval_horizontal(column,row,3)
            if result[0]:
                result.append([column,row])
                return result
        if row < 3:
            result = self._eval_vertical(column,row,3)
            if bool(result[0]):
                result.append([column,row])
                return result
        if column < 4 and row < 3:
            result = self._eval_diagonal_up(column,row,3)
            if result[0]:
                result.append([column,row])
                return result
        if column < 4 and row > 2 and row < 6:
            result = self._eval_diagonal_down(column,row,3)
            if result[0]:
                result.append([column,row])
                return result
        return [False,0]
        
    def _eval_grid(self): #Method to evaluate if someone has won. returns bool and the start and end cells of the win
        for c in range(7):
            for r in range(6):
                if self.connect_grid[c][r]:
                    result = self._eval_cell(c,r)
                    if result[0]:
                        return result
        return [False,0]
        
    def _drop_piece(self,column): #Searches a given column for a piece that needs to move down
        for i in range(6,0,-1):
            if self.connect_grid[column][i]:
                if not self.connect_grid[column][i-1]:
                    self.connect_grid[column][i-1] = self.connect_grid[column][i]
                    self.connect_grid[column][i] = None
                    return True
                elif i == 5:
                    self.connect_grid[column][i+1] = '-'
        return False
        
    def _animate_drop_piece(self,column): #Method to animate the dropping of a piece into the grid.
        go = True
        while go == True:
            sleep(.150)
            go = self._drop_piece(column)
            self._refresh_gui()

    def _get_winning_move(self,end_cell,start_cell): #works with data returned by eval methods to get the 4 cells in the grid that won the game
        cell_list = [end_cell,start_cell]
        if end_cell[0] == start_cell[0]:
            cell_list.append([start_cell[0],start_cell[1]+1])
            cell_list.append([start_cell[0],start_cell[1]+2])
        elif end_cell[1] == start_cell[1]:
            cell_list.append([start_cell[0]+1,start_cell[1]])
            cell_list.append([start_cell[0]+2,start_cell[1]])
        elif end_cell[0] > start_cell[0]:
            cell_list.append([start_cell[0]+1,start_cell[1]+1])
            cell_list.append([start_cell[0]+2,start_cell[1]+2])
        else:
            cell_list.append([start_cell[0]+1,start_cell[1]-1])
            cell_list.append([start_cell[0]+2,start_cell[1]-2])
        input('winning cells: %s' % cell_list)
        return cell_list

    def _show_winning_move(self,cell_list): #Sets all grid values to 'NoneType', except the winning 4 cells.
        for c in range(7):
            for r in range(7):
                matched = False
                for cell in cell_list:
                    print('evaluating cell %s' % cell)
                    if [c,r] == cell:
                        matched = True
                if not matched:
                    self.connect_grid[c][r] = None

    def _print_grid(self): #Method to write the grid to Console
        top = '   |'
        for c in range(7):
                if not self.connect_grid[c][6]:
                    top = top + str(c+1) + '|'
                else:
                    top = top + str(self.connect_grid[c][6]) + '|'
        print(top)
        for r in range(5,-1,-1):
            output = '   |'
            for c in range(7):
                if not self.connect_grid[c][r]:
                    output = output + '  '
                else:
                    output = output + str(self.connect_grid[c][r]) + ' '
            output = output[:-1] + '|'
            print(output)
        print('    TTTTTTTTTTTTT ')

    def _print_banner(self): #prints the banner
        for i in range(len(self.banner)):
            print(self.banner[i])
        
    def _ask_for_move(self): #Asks Human for input and returns spot number to put next piece
        avail_list = []
        for c in range(7):
            if not self.connect_grid[c][6]:
                avail_list.append(c+1)
        print('Where would you like to move?')
        while True:
            print('Available spots: %s' % avail_list)
            spot = input(' > ')
            try:
                if int(spot) in avail_list:
                    return int(spot) - 1
            except:
                print('Input not recognized...')

    def _refresh_gui(self): #clears console and prints banner, prompt, and grid
        system('cls')
        self._print_banner()
        if not self.winner:    
            print("  It is %s's turn" % self._current_turn)
        else:
            print("  %s Won The Game!" % self._current_turn)
        print('\n')
        self._print_grid()

    def _check_for_winner(self): #checks to see if someone has won the game and sets the "winner" variable if there is. Also passes turn to next player if nobody had won
        results = self._eval_grid()
        if results[0]:
            self.winner = self._piece_dict[self.connect_grid[results[1][0]][results[1][1]]]
            self._show_winning_move(self._get_winning_move(results[1],results[2]))
            self._refresh_gui()
            return True
        else:
            if self._current_turn == 'Human':
                self._current_turn = 'AI'
            else:
                self._current_turn = 'Human'
            return False

    def play_game(self): #Master command to start game and loop through player's turns
        while self.winner == None:
            self._refresh_gui()
            move = self._ask_for_move()
            self._set_piece(move,self.player)
            self._animate_drop_piece(move)
            if not self._check_for_winner():
                print(self.connect_grid)
                opponentMove = connect_4_cpu.getBestMove(self.connect_grid)
                self._set_piece(opponentMove,self.opponentPiece)
                self._animate_drop_piece(opponentMove)
                self._check_for_winner()

mygrid = ConnectGame()
mygrid.play_game()
