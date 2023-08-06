from grid import Grid
import cProfile


grid_format_1 = [
        ['M','A','P','O'],
        ['E','T','E','R'],
        ['D','E','N','I'],
        ['L','D','H','C']
    ]

grid_format_2 = [
        ['M','A','P'],
        ['E','T','E'],
        ['D','E','N'],
        
    ]

grid_format_3 = [
        ['M','A','P','O', 'A'],
        ['E','T','E','R', 'L'],
        ['D','E','N','I', 'M'],
        ['L','D','H','C', 'O'],
        ['L','D','H','C', 'P']
    ]

# Create grid instance
grid = Grid(existing_array=grid_format_2)

grid.print_grid()

# Search for all words in the grid
words = grid.find_all_words()
sortedwords = sorted(words, key=len)

# for word in sortedwords:
#     print(word)

# sortedwords = sorted(words, key=len)
# print(f"\nWords found: {len(words)}")
# print(f"Shortest word: {sortedwords[0]}")
# print(f"Longest word: {sortedwords[-1]}")