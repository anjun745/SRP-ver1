import random as rand
from openpyxl import Workbook
import xlrd

# how do I think?
# add mutations and maybe I wouldn't need how I think
# parents?
# add no mutation just ideals
# how do i mix mutation and inheritance?
wins = (['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g'])


def win_checker(side, blocks):
    for win in wins:
        w_c = 0
        for block in side:
            if block in win:
                w_c += 1
            if w_c > 2:
                return 'win'
    if not blocks:
        return 'tie'


successes = []
successes0 = []  # reduced, dont remove the wrongs, just keep the rights
draws = []  # the ones going into the dataset
x_success = []  # reduced
x_success0 = []
x_won = []  # the ones going into the dataset
o_success = []  # reduced
o_success0 = []
o_won = []  # the ones going into the dataset


def populate():  # how to incorporate inheritance and mutation?
    generation = ({'x_won': []}, {'o_won': []}, {'draw': []})
    for game in range(100):
        blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        ongoing = True
        m_c = 0
        while blocks and ongoing:
            m_c += 1
            if m_c % 2:
                side = x_blocks
                side_key = 'x'
            else:
                side = o_blocks
                side_key = 'o'
            side[side_key].append(blocks.pop(blocks.index(rand.choice(blocks))))
            print(x_blocks, o_blocks)
            status = win_checker(side[side_key], blocks)
            if status == 'win':
                if side_key == 'x':
                    generation[0]['x_won'].append((x_blocks, o_blocks))
                    break
                else:
                    generation[1]['o_won'].append((x_blocks, o_blocks))
                    break
            elif status == 'tie':
                generation[2]['draw'].append((x_blocks, o_blocks))
                break
    return generation


def reduction(gen1, gen2):
    pass


def inheritance(gen_prev):
    return


def mutation(gen_prev):
    pass
