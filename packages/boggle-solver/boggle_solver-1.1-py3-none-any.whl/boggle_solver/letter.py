

class Letter():

    def __init__(self, letter, grid_pos, connected=[], letter_path=None):

        if letter==None:
            raise Exception("No letter provided")
        if letter_path==None:
            self.letter_path=letter
        else:
            self.letter_path=letter_path + letter
            
        self.letter = letter
        self.grid_pos = grid_pos
        self.words_to_position = ''

        # all grid positions (max=8, min=3) which have a valid connection
        self.connected_to = connected

