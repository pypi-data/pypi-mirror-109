import random
from pathlib import Path
from boggle_solver.letter import Letter

class Grid():

    def __init__(self, existing_array):
        self.grid=[] # a 2-dimensional array full of letters
        self.matrix = [] # a 2-dimensional array full of letter objects

        self.words = []

        # validates given grid
        if self.valid_grid(existing_array)!=None:
            raise Exception(self.valid_grid(existing_array))
        else:
            self.grid=existing_array

        # creates letter nodes
        self.matrix = self.fill_grid(self.grid)

        # fills letter nodes with their connected letters
        self.set_connected_letters()
    
    def fill_grid(self, grid):
        """Creates letter objects and creates matrix with these in"""
        row_count=0
        column_count=0

        new_grid = []
        for row in grid:
            new_row=[]
            row_count=0
            for cell in row:
                pos = (row_count, column_count)
                new_row.append(Letter(cell, pos))
                row_count += 1
            new_grid.append(new_row)
            column_count += 1
        
        return(new_grid)

    def set_connected_letters(self):
        """Gets the surrounding letter objects and assigns them to the letter objects"""
        
        for row in self.matrix:
            for letter in row:
                letter.connected_to=self.get_surrounding_letter_object(letter.grid_pos)

    def generate_grid(self):
        """Generates letters and inserts them into the grid"""
        grid = []

        return(grid)

    def valid_grid(self, grid):
        """takes input and verifies it as a valid grid"""

        try:
            if len(grid) != len(grid[0]):
                return 'grid not a square'
            else:
                for col in grid:
                    if len(col) != len(grid):
                        return 'grid not a square'
        except:
            return 'issue validating grid'

        
        for row in grid:
            for cell in row:
                if len(cell) != 1:
                    return f'Value ({cell}) is longer than 1'
                if not cell.isupper():
                    return f'Value ({cell}) is not upper case'

        return None

    def print_grid(self):

        for row in self.grid:
            print(row)

    def get_letter(self, grid_pos):
        """Get letter object from a given grid position"""

        try:
            letter = self.matrix[grid_pos[1]][grid_pos[0]]
            return(letter)
        except IndexError:
            return(None)
    
    def get_surrounding_letter_object(self, grid_pos):
        """Get all surrounding letter objects from a given position"""
        
        co_ords = self.get_surrounding_coords(grid_pos)

        surrounding_letters = []

        for co_ord in co_ords:
            surrounding_letters.append(self.get_letter(co_ord))

        return(surrounding_letters)


    def get_surrounding_coords(self, grid_pos):
        """Get the surrounding coordinates from a given position"""
        
        surrounding_coords = []
        x = grid_pos[0]
        y = grid_pos[1]

        start_x = x-1
        finish_x = x+2
        start_y = y-1
        finish_y = y+2

        for row in range(start_x, finish_x):
            for column in range(start_y, finish_y):
                
                valid = self.get_letter((row, column))
               
                if (row,column) != (x,y) and row >= 0 and column >= 0 and valid != None: # skips current pos
                    surrounding_coords.append((row, column))
        
        return(surrounding_coords)
    
    def valid_word(self, word):
        """Check if a given word exists"""
        word = word.upper()

        base_path = Path(__file__).parent
        file_path = (base_path / "words.txt").resolve()
        
        with open(file_path, "r") as f:
            for line in f:
                compare = line[:-1].upper() # removes \n
                if compare==word:
                    return(True)
                else:
                    continue
            return(False)

    def valid_start(self, letters):
        """Check if the letters given could make the start of a word"""

        base_path = Path(__file__).parent
        file_path = (base_path / "words.txt").resolve()
        
        with open(file_path, "r") as f:
            for line in f:
                compare = line[:-1].upper() # removes \n


                if compare.startswith(letters):
                    return(True)
                else:
                    continue
            return(False)

    def find_all_words(self):
        """Loop through grid to find all possible words"""
        total = len(self.matrix)*len(self.matrix)
        counter=0
        for row in range(0,len(self.matrix)):
            for column in range(0,len(self.matrix)):
                current = (row, column) 
                current_letter = self.get_letter(current) 

                counter+=1
                       
                self.search([current_letter.grid_pos])
        return(self.words)


    def search(self, used_letters):
        """Recursive function to look through nodes for words"""

        string = ''
        for i in used_letters:
            string = string + self.get_letter(i).letter

        curr_pos = used_letters[-1]
        curr_letters = ''
        for l in used_letters:
            curr_letters = curr_letters + self.get_letter(l).letter
        
        # get surrounding letters
        surrounding = []
        around = self.get_surrounding_letter_object(curr_pos)
        for letter in around:
            if letter.grid_pos not in used_letters:
                surrounding.append(letter)

        for i in surrounding: 
            value = i.letter
            to_check = string + value
            
            if self.valid_word(to_check) == True and to_check not in self.words and len(to_check)>=3:
                self.words.append(to_check)
            
            if self.valid_start(to_check) == True:
                letters = used_letters.copy()
                letters.append(i.grid_pos)
                self.search(letters)
            # word = letters_so_far + self.get_letter(i).letter
    
if __name__ == "__main__":
    import cProfile
    grid_format = [
        ['M','A','P','O'],
        ['E','T','E','R'],
        ['D','E','N','I'],
        ['L','D','H','C']
    ]
    grid = Grid(existing_array=grid_format)