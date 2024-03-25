# using the rules and random to find the best plays
# I should add thinking about which blocks have more options
# how to improve o?
# not improving dynamically
# i need o to be doing the best for the optimal game, double improvement?
# double path check, the move after, from memory?
# make a core of items for understanding

import random as rand
from openpyxl import workbook
import pandas as pd

# move under the game loop for reset
# choose random and keep list for initial moves
initial_move_set = []
secondary_move_set = []

tie = False
x_win = False
o_win = False

x_wins = []
ties = []
o_wins = []

wins = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g']]

x_turn = True
# checks which side is placing and which set to check


def checker(checking):
    dangers = []    # the list of worried about

    if len(checking) >= 2:
        for move in checking:
            if move != checking[-1]:
                for sec_move_ind in range(checking.index(move)+1, len(checking)):
                    # checking blocks
                    for possible_danger in wins:
                        if move in possible_danger and checking[sec_move_ind] in possible_danger:
                            if possible_danger not in dangers:
                                dangers.append(possible_danger)
    return dangers


def blocking_placing(watching):
    options = []

    if watching:
        for danger in watching:
            for taken in side:
                if taken != side[-1]:
                    for sec_taken_ind in range(side.index(taken)+1, len(side)):
                        if taken in danger and side[sec_taken_ind] in danger:
                            danger.pop(danger.index(taken))
                            danger.pop(side[sec_taken_ind])
                            return danger[0]
                        elif taken in danger or side[sec_taken_ind] in danger:
                            # will later use random to choose
                            for win in wins:
                                safety_count = 2
                                for attempt in side:
                                    for enemy_spot in other:
                                        if attempt in win:
                                            if enemy_spot in win:
                                                safety_count -= 1
                                if safety_count == 0 and attempt:
                                    win.pop(win.index(attempt))     # problem is here
                                    options.append(win)
                    return options
    else:
        if blocks:
            return rand.choice(blocks)
        else:
            return 'tie'


def placing_detecting(game):

    if len(blocks) == 0:
        return 'tie'

    if len(side) > 0:

        for attempt in side:
            temp_win_list = []
            for win in wins:
                if attempt in win:
                    temp_win_list.append(side)
            for trying in temp_win_list:
                till_win = 3
                for trying_block in side:
                    if trying_block in trying:
                        till_win -= 1
                    if till_win == 0:
                        if side == initial_move_set:
                            return initial_move_set
                        else:
                            return secondary_move_set

        for win in wins:
            win_counter = 0
            for attempt in side:
                if attempt in win:
                    win_counter += 1
            if win_counter == 2:
                for left_2_fill in win:
                    if left_2_fill not in side:
                        side.append(left_2_fill)
                        blocks.pop(blocks.index(left_2_fill))
                        return

        if isinstance(block, list) and block:
            choice = rand.choice(block)[rand.randint(0, 1)]
            side.append(choice)
            blocks.pop(blocks.index(choice))
            return

        elif block:
            side.append(block)
            return

    else:
        side.append(rand.choice(blocks))
        return


def temp_check():
    to_pop = []
    for blocc in blocks:
        if blocc in side or other:
            to_pop.append(blocc)
    for poping in to_pop:
        blocks.pop(blocks.index(poping))


game_count = 0
while game_count <= 1:  # stuck, not moving on
    blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    game_count += 1
    # while len(blocks):
    # for run in range(9):
    while True:
        if x_turn:
            side = initial_move_set
            other = secondary_move_set
            checked = checker(other)
            block = blocking_placing(checked)
            result = placing_detecting(side)
            print(side, 'xn')

            if result == 'x':  # prob dont need this
                temp_list_end = [initial_move_set, secondary_move_set]
                x_wins.append(temp_list_end)
                break
            elif result == 'tie':
                temp_list_end = [initial_move_set, secondary_move_set]
                ties.append(temp_list_end)
                break
            elif result == 'o':
                temp_list_end = [initial_move_set, secondary_move_set]
                o_wins.append(temp_list_end)
                break
            x_turn = False

        else:
            side = secondary_move_set
            other = initial_move_set
            checked = checker(other)
            block = blocking_placing(checked)
            result = placing_detecting(side)
            print(side, 'on')

            if result == 'x':   # prob dont need this
                temp_list_end = [initial_move_set, secondary_move_set]
                x_wins.append(temp_list_end)
                print(temp_list_end, 'x')
                break
            elif result == 'tie':
                temp_list_end = [initial_move_set, secondary_move_set]
                ties.append(temp_list_end)
                print(temp_list_end, 't')
                break
            elif result == 'o':
                temp_list_end = [initial_move_set, secondary_move_set]
                print(temp_list_end, 'o')
                o_wins.append(temp_list_end)
                break
            x_turn = True
        temp_check()

# print(x_wins[:int(len(x_wins)/2):])
# print(o_wins[:int(len(o_wins)/2):])
# print(ties[:int(len(ties)/2):])
