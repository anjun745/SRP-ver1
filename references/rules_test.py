import random as rand
# wouldn't making a program for defence be more legit?
wins = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g']]
blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

x_blocks = [blocks.pop(blocks.index(rand.choice(blocks))), blocks.pop(blocks.index(rand.choice(blocks)))]
o_blocks = [blocks.pop(blocks.index(rand.choice(blocks)))]

print(x_blocks, ':', o_blocks, '||', blocks)

# write something to remove impossible options in which o has spots
# blocking
for win in wins:
    print('|', win, '|')
    until_win = 0
    for item in x_blocks:       # does this check if a block is in o?
        print(item)
        if item in win:

            print('with', item, win)

            until_win += 1
    if until_win >= 2:
        for item in x_blocks:
            if item in win:
                win.pop(win.index(item))     #DO NOT DELETE FULL LINE, DELETE PRINT

        print('\n', win, 'danger\n')

        if win[0] in blocks:
            print(win, 'for o')
            o_blocks.append(win[0])    # side/turn dependent
        else:
            win_list = []
            for win in wins:    # should be fine
                until_win = 0
                for item in o_blocks:
                    if item in win:
                        until_win += 1
                        win.pop(win.index(item))
                    win_list.append([until_win, win])
            win_list.sort(reverse=True)
            o_blocks.append(rand.choice(win_list[0][1]))
        break  # if o has more than 1 choice to fill o is fked
    # if it hits 3 its a win
# print(o_blocks)
# attacking
# o_blocks = ['e']
# x_blocks = ['c']

print('wins', wins)     # there seems to be some issues here

for win in wins:
    possible_w = True

    print(win, 'win')   # there is an error with what could be in here

    for x in x_blocks:
        if x not in win:
            possible = False

            print(f'{x} solution', 'x')

            break
        for o in o_blocks:
            if o in win:
                possible = False
                break


