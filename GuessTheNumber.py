# GuessTheNumber.py
# A game in which a player guesses a random number within a certain number of chances.

import random
import math

# Constants.
#MIN_INT = 1
#MAX_INT = 1000
MAX_GUESSES = 10
GUESS_STRS = { 0 : 'first',
               1 : 'second',
               2 : 'third',
               3 : 'fourth',
               4 : 'fifth',
               5 : 'sixth',
               6 : 'seventh',
               7 : 'eighth',
               8 : 'ninth',
               9 : 'tenth' }

""" 
    int  getInt(str)
    
    Displays prompt and asks for an integer.
    Prints an error and asks again if the user enters anything other than an integer.
"""
def getInt(prompt):

    while(True):
        try:
            return int(input(prompt))
        except:
            print('You must enter an integer.')

player_won = False

print('Hello player!')
print('')



MIN_INT = getInt('What do you want the minimum of the range to be? ')
MAX_INT = getInt('What do you want the maximum of the range to be? ')

print('')
print(f'Guess a number between {MIN_INT} and {MAX_INT}.  You have {MAX_GUESSES} tries.')
print('')
# Generate a random number.
random_number = random.randint(MIN_INT,MAX_INT)

for i in range(0,MAX_GUESSES):
    guess_int = getInt(f'What is your {GUESS_STRS[i]} guess? ')

    if guess_int > random_number:
        print("Guess is too high.")
    elif guess_int < random_number:
        print('Your guess is too low.')
    else:
        print('')
        print('Congratulations, you got it!!!!')
        player_won = True
        break

if not player_won:
    print('')
    print(f'Sorry, it was {random_number}.  Better luck next time!')



