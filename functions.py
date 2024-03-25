import random as rand

wins = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
                         ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
                         ['a', 'e', 'i'], ['c', 'e', 'g']]
blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
x_blocks = []
o_blocks = []


def win_checker(placed, plc=None):
    for win in wins:
        counter = 0
        for block in placed:
            if block in win:
                counter += 1
        if counter == 3:
            return 'win'
        if plc and counter == 2:
            return win
    return 'ongoing'


# 'commented out because dupe'
# # def block_choosing(side, other):
# #     for block in x_blocks:  # checking for dupes
# #         if block in blocks:
# #             blocks.pop(blocks.index(block))
# #     for block in o_blocks:  # checking for dupes
# #         if block in blocks:
# #             blocks.pop(blocks.index(block))
# #
# #     if type(win_checker(side, 'plc')) == list:  # if next to win
# #         for block in win_checker(side, 'plc'):
# #             if block in blocks:
# #                 side.append(blocks.pop(blocks.index(block)))
# #                 return
# #     if type(win_checker(other, 'opp')) == list:  # if there are no wins and the opp is one away
# #         for block in win_checker(other, 'opp'):
# #             if block in blocks:
# #                 side.append(blocks.pop(blocks.index(block)))
# #                 return
# #     # be careful with testing, if the blocks are "one away", this part would not be reached
# #
# #     possible_routes = []
# #     for win in wins:
# #         go_for = True
# #         for needed in win:
# #             if needed in side or needed in other:
# #                 go_for = False
# #         if go_for:
# #             possible_routes.append(win)
# #
# #     if possible_routes:
# #         side.append(blocks.pop(blocks.index(rand.choice(rand.choice(possible_routes)))))
# #         return
# #     elif not possible_routes and blocks:
# #         side.append(blocks.pop(blocks.index(rand.choice(blocks))))
# #         return
# #     else:
# #         # print('tie')
# #         return 'tie'

