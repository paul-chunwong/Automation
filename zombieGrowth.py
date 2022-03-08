import random
from random import randrange
import numpy
from PIL import Image
from numpy import random
import pygame
import numpy as np  # we'll use numpy arrays as the basis for our grids.
import sys
from typing import Tuple, List
from dataclasses import dataclass, field

# Define some colors, mostly useful for testing
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# # Set the number of states to use within each cell
# states = 2  # we leave this as a global variable since it doesn't change.


# Things that can be changed: number of states, grid dimensions, square size,
# padding, neighbors function, rules function, grid initialization function.

class grid:
    gridSize: Tuple[int, int]  # columns, rows == x,y
    data: np.ndarray
    generations: int

    def __init__(self, size, setup):
        self.gridSize = size
        self.data = setup
        # your code here...initialize data to the result of executing setup function on input size
        self.generations = 0


# # Testing for grid constructor:
# A1 = grid([5,5],[[1,2],[2,3]])
# print(A1.gridSize)
# print(A1.data)
# print(A1.generations)


# --------------------------------------------------------------------
# Initialization functions -- used by the constructor. Only one is used
# in any game definition. You may add your own for the creative exercise.
# --------------------------------------------------------------------

# function: randStart
# Purpose: employed by grid __init__ (constructor) to give initial value to data
# param: size
# returns: an np array of size size, whose values are uniformly selected from range(states)
def randStart(size):
    # your code here
    arr = random.randint(states, size=(size, size))
    return arr

# print(randStart(5))


# function: glideStart
# Purpose: employed by grid __init__ (constructor) to give initial value to data
# param: size
# returns: an np array of size size, whose values are all zero, except for positions
# (2,0), (0,1), (2,1), (1,2), and (2,2), whose values are 1. Intended to be used
# on a game w 2 states.
def glideStart(size):
    # your code here
    arr = numpy.tile(0, (size, size))
    arr[0][2] = 1
    arr[1][0] = 1
    arr[1][2] = 1
    arr[2][1] = 1
    arr[2][2] = 1
    return arr

# print(glideStart(10))


def zombieStart(size):
    # your code here
    arr = numpy.tile(0, (size, size))
    arr[20][20] = 1
    return arr



# --------------------------------------------------------------------
# Rule functions -- used by the evolve function. Only one is used
# in any game definition. You MUST add a new one for the creative exercise.
# --------------------------------------------------------------------

# function: ruleGOL
# purpose: applies a set of rules given a current state and a set of tallies over neighbor states
# params: cell, an element from range(states), where states is the global variable
#           tallies, tallies[k] = number of neighbors of state k, for all k in the range of states
# returns: a new state based on the classic rules of the game of life.
#           See https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# Note: assumes a two-state game, where 0 is "dead" and 1 is "alive"

def ruleGOL(cell, tallies):
    if cell == 0 and tallies[1] == 3:
        return 1
    elif cell == 1 and tallies[1] < 2:
        return 0
    elif cell == 1 and tallies[1] > 3:
        return 0
    elif cell == 1 and tallies[1] == 3:
        return 1
    elif cell == 1 and tallies[1] == 2:
        return 1
    else:
        return 0


# tallies1 = [2, 6]    # [number of neighbors that are dead, number of neighbors that are alive]
# tallies2 = [4, 4]
# tallies1[0] =  # number of neighbors that are dead
# tallies1[1] =  # number of neighbors that are alive


# function: ruleCycle
# purpose: applies a set of rules given a current state and a set of tallies over neighbor states
# params: cell, an element from range(states), where states is the global variable
#           tallies, tallies[k] = number of neighbors of state k, for all k in the range of states
# returns: if k is the current state, returns k+1 if there is a neighbor of state k+1, else returns k

def ruleCycle(cell, tallies):
    # cell = 4
    # tallies = [1, 2, 3, 2, 0]

    if cell == (len(tallies) - 1):
        if tallies[0] > 0:
            return 0
        else:
            return cell
    else:
        if tallies[cell + 1] > 0:
            return cell + 1
        else:
            return cell


# # example for cell (cell number cannot be bigger than state-1)
# cell_1 = 3
# cell_2 = 4
# cell_3 = 2
# cell = 40
# cell = 35
#
# # example for state
# if state  == 5:
# tallies1 = [3, 2, 2, 0, 1]      # Every tallies must have a sum of 8 no matter how long the states are
#
# # Logic:
# if cell_1+1 (4) (==1):   # If cell + 1 in the position of tallies equals 1 (>0), return cell + 1
#     return cell_1 + 1
# if cell_2+1 (5) (==len(tallies)):   # If cell + 1 in the position of tallies equals to the length of tallies,
# # check the first item in tallies, if the first item is > 0, return 0, otherwise return the original cell value
#     return 0 (since tallies[0] > 0)
# if cell_3+1 (3) (==0):   # If cell + 1 in the position of tallies equals 0, return the original cell value
#     return cell_3
# else:
#     return cell_1   # All other conditions return original value of cell


def ruleZombie(cell, tallies):
    return random.randint(states, size=1)


# --------------------------------------------------------------------
# Neighbor functions -- used by the evolve function. Only one is used
# in any game definition. You may add your own for the creative exercise.
# --------------------------------------------------------------------
# returns a list of neighbors in a square around x,y
def neighborSquare(x, y):
    neighborSet = [[x + 1, y], [x + 1, y + 1], [x, y + 1], [x - 1, y + 1], [x - 1, y], [x - 1, y - 1], [x, y - 1],
                     [x + 1, y - 1]]
    return neighborSet


# returns a list of neighbors in a diamond around x,y (NWSE positions)
def neighborDiamond(x, y):
    neighborSet = [[x + 1, y], [x, y + 1], [x - 1, y], [x, y - 1]]
    return neighborSet


# function: tally_neighbors
# purpose: counts a given cell's the neighbors' states
# params: grid, an np array of data from a grid, containing states of all cells
#         position, the current cell position (a Tuple)
#         neighborSet, a function that when called on position x,y returns a list of x,y's neighbors
# returns: a list whose entries, tally[k] are the number of valid neighbors of x,y whose state is k.
# Note: neighborSet may not necessarily return *valid* neighbors. It's tally_neighbor's job to check
# for validity.

def tally_neighbors(grid: np.array, position: Tuple, neighborSet: List[Tuple]) -> List:
    # your code here
    tallies = []
    # print(grid)
    # print(position)
    # print(neighborSet)

    # Filter the valid neighbors (preventing out of bound conditions):
    maxBound = len(grid)
    # print(maxBound)

    validNeighborList = []
    for j in neighborSet:
        for k in j:
            if k < maxBound and k >= 0:
                validNeighborList.append(j)
    # print(validNeighborList)

    finalValidNeighborList = []
    for j in validNeighborList:
        if validNeighborList.count(j) == 2:
            finalValidNeighborList.append(j)
    # print(finalValidNeighborList)

    finalValidNeighborList2 = []
    for i in range(0, len(finalValidNeighborList)):
        if i % 2:
            finalValidNeighborList2.append(finalValidNeighborList[i])

    # print(finalValidNeighborList2)

    # Finding the largest state in the grid:
    maxState = 0
    for j in grid:
        for k in j:
            if k > maxState:
                maxState = k
    # print(maxState)


    # Create the tallies with the correct length:
    talliesLength = maxState + 1
    tallies = [0] * talliesLength
    # print(tallies)

    # Get the final tallies list from neighborSet list
    for i in range(0, len(finalValidNeighborList2)):
        current_position = finalValidNeighborList2[i]
        for i2 in range(len(tallies)):
            if grid[current_position[1]][current_position[0]] == i2:
                tallies[i2] = tallies[i2]+1
    # print(tallies)

    return tallies


# tally_neighbors([[1,6,0,0,2,3],
#                  [2,8,8,9,11,2],
#                  [7,3,2,3,4,8],
#                  [7,3,2,3,4,8],
#                  [7,3,2,3,4,8],
#                  [7,3,2,3,4,8]],[0,5], neighborSquare(0,5))

# tally_neighbors([[1,6,0],
#                  [2,8,8],
#                  [7,3,2]],[1,1], neighborSquare(1,1))




# student: putting it all together.
# function: evolve
# purpose: to increment the automata by *one* time step. Given an array representing the automaton at the
# start of the time step (the start grid), this function creates an array for the end of the time step
# (the end grid) by applying the rule specified in function apply_rule to every position in the array.
# Note that all rule evaluation is done on the start grid, but the new state is set in the end grid.
# This function *changes* the input parameter to the new state.
# The grid's generations variable should be incremented every time the function is called. (This variable
# may only be useful for debugging--there is a lot we *could* do with it, but our application doesn't use it.)

def evolve(gr, apply_rule, neighbors):
    print(gr.data)
    result1DGrid = []
    length = gr.gridSize[0]
    gridArray = gr.data
    for j in range(0, length):
        for k in range(0, length):
            tallies = tally_neighbors(gr.data, (k, j), neighbors(k, j))
            result = apply_rule(gr.data[j][k], tallies)
            result1DGrid.append(result)
    # print(result1DGrid)

    finalGrid = np.array(result1DGrid).reshape(len(gridArray), len(gridArray))
    # print(finalGrid)

    gr.data = finalGrid
    print(gr.data)

# evolve(grid((10,10), glideStart(10)),ruleGOL,neighborSquare)




# function draw_block
# purpose: draw a rectangle of color acolor for *grid* location x,y. Uses globals pad and sqSize.
# function solution is:     pygame.draw.rect(screen, acolor,
#   [upper left horiz pixel location, upper left vertical pixel location, sqSize, sqSize])
# returns: nothing
def draw_block(x, y, acolor):
    pygame.draw.rect(screen, acolor, [x*(sqSize+pad), y*(sqSize+pad), sqSize, sqSize])
    # pygame.draw.rect(screen, acolor, [0, 0, sqSize, sqSize])
    return

# draw_block(5,5,GREEN)



# function: draw
# purpose: translates the game representation from the grid, to an image on the screen
# param: gr, a grid. for every position in gr.data, computes a color based on the state
# in that location, and then makes a call to draw_block to place that color into the pygame
# screen. Also passes the grid location so draw_block can compute the correct screen location.
# The new color is represented in HSVA (see https://www.pygame.org/docs/ref/color.html#pygame.Color.hsva
# and has hue h = (360 // states) * current state, s = 100, and v = 50 (we just left A of HSVA
# at its default value). You may want to experiment with these values for artistic effect. :)
# returns: nothing
def draw(gr):
    size = gr.gridSize
    for i in range(size[0]):
        for j in range(size[1]):
            if gr.data[i][j] == 0:
                draw_block(i, j, BLUE)
            else:
                draw_block(i, j, RED)
    return None

# following are the game, grid, and screen parameters for the problem

# Set the number of states to use within each cell
states = 2  # we leave this as a global variable since it doesn't change.

# words to display on the window
pygame.display.set_caption("CPSC203 Life")

# the game state is maintained in a grid object.
# grid data values will be updated upon every click of the clock.
# parameters are the (width, height) dimensions of the grid, and a
# function that initializes the start state
# g = grid((40, 40), randStart(40))
g = grid((40, 40), zombieStart(40))
# print(g.gridSize[0])
# print(g.gridSize)


# drawing parameters that determine the look of the grid when it's shown.
# These can be set, but defaults are probably fine
sqSize = 3  # size of the squares in pixels
pad = sqSize // 5 # the number of pixels between each square

# computed from parameters above and grid g dimensions
s = (sqSize*g.gridSize[0]+pad*(g.gridSize[0]-1),sqSize*g.gridSize[1]+pad*(g.gridSize[1]-1)) # YOUR CODE HERE! dimensions of pixels in screen window (width,height)
# s = (225,225)
screen = pygame.display.set_mode(s)  # initializes the display window

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# given: necessary for gracefully ending game loop (pygame)
def handleInputEvents():
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close...
            sys.exit(0)  # quit

# some variables you probably won't want to change
frameCount = 0
desiredGifLength = 200
frameRate = 60
frames = []

# -------- Main Program Loop -----------
while True: # runs continually until stopped
    # --- Main event loop
    handleInputEvents()

    # # --- Draw the grid
    # # this function loops over the data in the grid object
    # # and draws appropriately colored rectangles.
    draw(g)

    # --- Game logic should go here
    # evolve( g, rule, neighbors)
    # g -- an object of type grid, previously initialized to hold data start state
    # rule -- a function that applies the game rule, given a cell state and a neighbor tally
    # neighbors -- a function that returns a list of neighbors relative to a given x,y position.
    # evolve(g, ruleZombie, neighborDiamond)
    evolve(g, ruleZombie, neighborSquare)
    # evolve(g, ruleCycle, neighborDiamond)


    # --- Mysterious reorientation that every pygame application seems to employ
    pygame.display.flip()

    # --- Uncomment code below to save a GIF of your custom automaton
    if frameCount < desiredGifLength:
        pygame.image.save(screen, "temp.png")
        frames.append(Image.open("temp.png"))
    else:
        frames[0].save('custom.gif', format='GIF',
                       append_images=frames[1:], duration=1000/frameRate,
                       save_all=True, loop=0)
    frameCount += 1


    # --- Limit to 60 frames per second
    clock.tick(frameRate)

# Close the window and quit.
pygame.quit()
