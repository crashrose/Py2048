from enum import Enum
from random import randint
from tkinter import Frame, Label, Tk


# class to return necessary information for traversing array based on selected direction
class direction():
    def __init__(self, direction):
        self.dir_name = direction
        dir_data = {'LEFT':{'start': 0, 'direction': 1, 'calc_by': 'row', 'calc_by_inv':'col', 'calc_reverse':False},
             'RIGHT':{'start': 3, 'direction':-1, 'calc_by': 'row', 'calc_by_inv':'col', 'calc_reverse':True},
             'UP':{'start': 0, 'direction': 1, 'calc_by': 'col', 'calc_by_inv':'row', 'calc_reverse':False},
             'DOWN':{'start': 3, 'direction':-1, 'calc_by': 'col', 'calc_by_inv':'row', 'calc_reverse':True}
             }
        # populate attributes
        self.Direction = dir_data[self.dir_name]
        self.start = self.Direction['start']
        self.direction = self.Direction['direction']
        self.calc_by = self.Direction['calc_by']
        self.calc_by_inv = self.Direction['calc_by_inv']
        self.calc_reverse = self.Direction['calc_reverse']

# Values for current turn label string
class move_type(Enum):
    INITIAL = "To begin, use the arrow keys to move."
    REGULAR = "Use the arrow keys to move."
    INVALID = "That is not a valid move, please choose a different direction. "
    GAME_OVER = "No more valid moves. Game over."
    
# main game class
class gameBoard:
    grid_values = {'row':0, 'col':0}
    display_array = {'r_c':0}
    emptyCellArray = [0]
    turn_count = 0
    total_score = 0
    game_over = False
    
    # core game play method called when arrow key is entered - bound to root tkinter element
    def game_play(self, event):
        # only perform game play if the game is not over
        # if so, perform shift and determine if the entered move is valid (i.e., results in a shift)
        if self.game_over == False:
            valid_move = self.shift(event.keysym.upper())
            
            # if the move is valid, update the display label 2d list, wait 150ms (to delay new gamepiece), then continue
            if valid_move == True:
                self.print_arrays()
                update_period_in_ms = 150
                self.main.after(update_period_in_ms, self.complete_turn)
        return
    
    # remainder of valid move actions after delay for added gamepiece
    def complete_turn(self):
        # add new gamepiece, update gui, and test to determine if the completed move ends the game
        self.add_value()
        self.root.update()
        self.turn_count += 1
        move_remains = self.remaining_move_test()
        if move_remains == False:
            self.turn_label['text'] = move_type['GAME_OVER'].value
            self.game_over = True

    # initialization of class populates initial 2d list and creates, binds, and runs the tkinter display elements        
    def __init__(self, root):
        
        # create labels and frames with initial values and bind them
        self.root = root
        self.main = Frame(root)
        self.header = Frame(root)
        self.header_label = Label(self.header, text='2048 Game')
        self.score_label = Label(self.header, text='Score: 0')
        self.turn_label = Label(self.header, text=move_type['INITIAL'].value, wraplength=150, height=3)        
        self.header.pack()
        self.header_label.pack()
        self.score_label.pack()
        self.turn_label.pack()
        self.main.pack()
        self.root.bind('<Left>', self.game_play)
        self.root.bind('<Right>', self.game_play)
        self.root.bind('<Up>', self.game_play)
        self.root.bind('<Down>', self.game_play)
        
        # create initial row and col 2d lists and start with a 2 in a random gamepiece
        self.grid_values['row'] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.grid_values['col'] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]       
        rand_x = self.get_rand(0, 3, "x_val")
        rand_y = self.get_rand(0, 3, "y_val")
        self.grid_values['row'][rand_x][rand_y] = 2
        self.grid_values['col'][rand_y][rand_x] = 2

        # create cells (labels) for gamepiece values and print initial values
        for i in range (0, 4):
            for j in range (0, 4):
                cell_name = 'r' + str(i) + '_c' + str(j)
                self.display_array.update({cell_name:Label(self.main, width=6, height=2, borderwidth=2, relief='ridge')})
                self.display_array[cell_name].grid(row=i, column=j)
        self.print_arrays()

        # start tkinter gui
        self.root.mainloop()

    # sets the display values for each tkinter cell text        
    def print_arrays(self):
        for i in range (0, 4):
            for j in range (0, 4):
                cell_name = 'r' + str(i) + '_c' + str(j)
                if self.grid_values['row'][i][j] > 0:
                    cell_text = self.grid_values['row'][i][j]
                else:
                    cell_text = ""
                self.display_array[cell_name]['text'] = cell_text
        return
    
    # generates random numbers for new game piece locations and values
    def get_rand(self, mininum, maximum, rand_type):
        val = randint(mininum, maximum)
        
        # if the type is cell val, returns 2, 4, or 8 based on 85%, 12%, and 3% probability, respectively
        if (rand_type == "cell_val"):
            if (val <= 85):
                val = 2
            elif (val <= 97):
                val = 4
            elif (val <= 100):
                val = 8
        return val

    # performs the actual shift to slide game pieces in the direction that user selected 
    # returns false for invalid (i.e., there were no cells to shift to in that direction)
    def shift(self, dir_name):
        self.dir_name = dir_name
        self.direction = direction(dir_name)
        move_made = False
        
        # populate initial editable temp 2d lists from current values
        # curValsInv is the 2d list of rows if direction is calc'ed by columns, and vice versa
        curVals = self.grid_values[self.direction.calc_by][:][:]
        curValsInv = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i in range (0, 4):
            
            # populate values for current row or column, reverse if appropriate, and remove empty cells
            curList = curVals[i][:]
            if (self.direction.calc_reverse):
                curList.reverse()
            curList = list(filter((0).__ne__, curList))
            
            # for each item in the row or column, test if the current item has the same value as the next item
            # if so, double the value of the current item and remove the next item from the list
            j = 0
            while (j < len(curList) - 1 and len(curList) > 0):
                if (curList[j] == curList[j + 1]):
                    curList[j] = (curList[j] * 2)
                    self.total_score += curList[j]
                    curList.pop(j + 1)

                j += 1
                
            # add 0 values to the end of the list to make it complete and reverse back to original dir if appropriate
            vals_to_add = (4 - len(curList)) * [0]
            curList.extend(vals_to_add)
            if (self.direction.calc_reverse):
                curList.reverse()
                
            # set the new list values to the current row or col of the temp array and populate the inverse values
            curVals[i] = curList[:]
            curValsInv[0][i] = curVals[i][0]
            curValsInv[1][i] = curVals[i][1]
            curValsInv[2][i] = curVals[i][2]
            curValsInv[3][i] = curVals[i][3]
            self.score_label['text'] = 'Score: ' + str(self.total_score)
            
        # if the gameboard 2d list has been modified, update the class row/col lists, update the label, and return true
        # otherwise, set label to invalid move and return false without updating class row/col lists
        if (curVals != self.grid_values[self.direction.calc_by]):
            self.grid_values[self.direction.calc_by] = curVals[:][:]
            self.grid_values[self.direction.calc_by_inv] = curValsInv[:][:]
            move_made = True
            self.turn_label['text'] = move_type['REGULAR'].value
        else:
            move_made = False
            self.turn_label['text'] = move_type['INVALID'].value
        return move_made

    # populates list of empty cells
    def find_empty_cells(self):
        self.emptyCellArray[:] = []
        q = 0
        
        # iterate through 2d list by row and if a cell is empty, copy the position to a new value in dictionary of empty cells
        for m in range (0, 4):
            for n in range (0, 4):
                if (self.grid_values['row'][m][n] == 0):
                    emptyValHolder = {'row': m,
                                      'col': n
                                      }
                    q += 1
                    self.emptyCellArray.append(emptyValHolder.copy())
                    emptyValHolder.clear()
        return

    # adds new gamepiece to board
    def add_value(self):
        self.find_empty_cells()
        if (len(self.emptyCellArray) > 0):
            # get random numbers for the new value and the cell that it will populate
            # gather the row/col coordinates of the cell from the empty cell dictionary
            val = self.get_rand(0, 100, "cell_val")
            loc = self.get_rand(0, len(self.emptyCellArray) - 1, "loc")
            x_val = self.emptyCellArray[loc]['row']
            y_val = self.emptyCellArray[loc]['col']
            
            # set the value of the cell in the class row/col 2d list, 
            # remove used item from empty cell dictionary, and update cell label with value
            self.grid_values['row'][x_val][y_val] = val
            self.grid_values['col'][y_val][x_val] = val
            self.emptyCellArray.pop(loc)
            cell_name = 'r' + str(x_val) + '_c' + str(y_val)
            self.display_array[cell_name]['text'] = str(val)
        return       
    
    # tests for any remaining moves which will indicate if game is over
    def remaining_move_test(self):
        move_test = False
        
        # if there are any empty cells, the test returns true. Otherwise,
        # test each cell to determine if its value is equal to an adjacent cell and can therefore be moved.
        # The loops will exit upon first instance of a possible move   
        if (len(self.emptyCellArray) != 0):
            move_test = True
        else:
            i = 0
            while i < 4 and move_test == False:
                j = 0
                while j < 4 and move_test == False:
                    if (i + 1 < 4):
                        if (self.grid_values['row'][i][j] == self.grid_values['row'][i + 1][j]):
                            move_test = True
                    if (j + 1 < 4):
                        if (self.grid_values['row'][i][j] == self.grid_values['row'][i][j + 1]):
                            move_test = True
                    j += 1
                i += 1
        return move_test

# create tkinter and core game objects
root = Tk()
gameBoard = gameBoard(root)