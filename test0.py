import random
c = []
# print(random.choice(c))
b = [[], [], [], [], [], [], [], [], ['e']]
for i in b:
    if not i:
        print(True)
b.remove('z')
b[3:6] = ['a', 'b', 'c']
print(len(b))
print(b)
print(b[3], b[4], b[5])
print(b[0:8])
# import random as rand
# import numpy as np
# from itertools import zip_longest
#
# wins = (['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],  # requirements, not possibilities
#         ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
#         ['a', 'e', 'i'], ['c', 'e', 'g'])
# blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
# blocks = np.arange(10)
# print(blocks)
# def win_checker(side, blocks):
#     if side == x_blocks:
#         side = x_blocks['x']
#     else:
#         side = o_blocks['o']
#     for win in wins:
#         w_c = 0
#         for block in side:
#             if block in win:
#                 w_c += 1
#             if w_c > 2:
#                 return 'win'
#     if not blocks:
#         return 'tie'
#
# def p():
#     for g in range(10):
#         blocks = []
#         print(win_checker(x_blocks, blocks))
# p()
#
# def win_checker(placed, plc=None):
#     if placed == x_blocks:
#         placed = x_blocks['x']
#     else:
#         placed = o_blocks['o']
#     doables = []
#     for win in wins:
#         counter = 0
#         for block in placed:
#             if block in win:
#                 print(block)
#                 counter += 1
#         if counter == 3:
#             return 'win'
#         if plc and counter == 2:
#             print(win)
#             print('!', x_blocks)
#             doables.append(win)
#     if doables:
#         return doables
#     return 'ongoing'
#
#
# def win_checker(placed, plc=None):
#     if placed == x_blocks:
#         placed = x_blocks['x']
#     else:
#         placed = o_blocks['o']
#     for win in wins:
#         counter = 0
#         for block in placed:
#             if block in win:
#                 counter += 1
#         if counter == 3:
#             return 'win'
#         if plc and counter == 2:
#             return win
#     return 'ongoing'
#
#
# def block_choosing(side, learned=None):  # i need some kind of unideal prevention module
#     if side == x_blocks:
#         side_ind = 0
#         side = x_blocks
#         side_key = 'x'
#         other = o_blocks
#     else:
#         side_ind = 1
#         side = o_blocks
#         side_key = 'o'
#         other = x_blocks
#
#     # checking for dupes
#     for block in x_blocks['x']:
#         if block in blocks:
#             blocks.pop(blocks.index(block))
#     for block in o_blocks['o']:
#         if block in blocks:
#             blocks.pop(blocks.index(block))
#
#     # hierarchy pt 1
#     if type(win_checker(side, 'plc')) == list:  # if next to win
#         for doable in win_checker(side, 'plc'):
#             for block in doable:
#                 if block in blocks:
#                     print('checkmate')
#                     side[side_key].append(blocks.pop(blocks.index(block)))
#                     return
#     if type(win_checker(other, 'opp')) == list:  # if there are no wins and the opp is one away
#         for block in win_checker(other, 'opp'):
#             if block in blocks:
#                 print('defended')
#                 side[side_key].append(blocks.pop(blocks.index(block)))
#                 return
#
#
# x_blocks = {'x': ['g', 'e', 'i']}
# o_blocks = {'o': ['d', 'c', 'h']}
# blocks = ['a', 'b', 'f']
# # print('win checker', win_checker(x_blocks, 'plc'))
# # block_choosing(x_blocks)
# # print(x_blocks, o_blocks)
