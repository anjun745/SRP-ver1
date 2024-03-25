import random as rand
import numpy as np

# variable function?
wins = (['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g'])
blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
board = [[], [], [], [], [], [], [], [], []]
population = [[], [], []]


def deduction(game):
    final = 1
    for taken in game:
        if taken:
            final += 1
    for ending in range(5, final-1):
        if win_checker(game[ending], final-1) == 'win':
            return game[ending]
    shoving = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    print(game)
    for slot in game:
        places_taken = 0
        for taken in game:
            if taken:
                places_taken += 1
            if win_checker(game[:places_taken], places_taken - 1) == 'win':
                game = game[:places_taken]
                for space in range(len(shoving) - len(game[:places_taken])):
                    game.append([])
                return game
        if not slot:
            while shoving:
                shove = shoving.pop(shoving.index(rand.choice(shoving)))
                if shove not in game:
                    game[game.index(slot)] = shove
                    break
        if win_checker(game[:places_taken+1], places_taken - 1) == 'win':
            game = game[:places_taken]
            for space in range(len(shoving) - len(game[:places_taken])):
                game.append([])
            return game
    print('draw', game)
    return game


def win_checker(game, turn):
    checking = []
    if turn % 2:
        for i in range(len(game)):
            if i % 2:
                checking.append(game[i])
    else:
        for i in range(len(game)):
            if not i % 2:
                checking.append(game[i])
    for win in wins:
        w_c = 0
        for block in checking:
            if block in win:
                w_c += 1
            if w_c > 2:
                population[turn % 2].append(game)
                return 'win'
    for placed in game[::-1]:
        if not placed:
            return
    return 'draw'


def mixer(mixing):
    g1 = rand.choice(mixing)
    g2 = rand.choice(mixing)
    l1 = 0
    l2 = 0
    d1 = 0
    # d2 = 0
    bowl = [[], [], [], [], [], [], [], [], []]
    for place in g1:
        if place:
            l1 += 1
    for place in g2:
        if place:
            l2 += 1
    if l1 >= l2:
        length = np.arange(l2)
        base = g2
        add_on = g1
    else:
        length = np.arange(l1)
        base = g1
        add_on = g2
    section_len = rand.choice(length)
    if len(length) - section_len > 0:
        d1 = rand.randrange(len(length) - section_len)
        # if len(length) - (d1 + section_len) > 0:
        #     pass
        #     # d2 = len(length) - (d1 + section_len)
    bowl[d1:(section_len + d1)] = base[d1:(section_len + d1)]
    for slot in add_on:
        if not bowl[add_on.index(slot)]:
            if slot not in bowl:
                bowl[add_on.index(slot)] = slot
            else:
                shoving = add_on.copy()
                while shoving:
                    attempt = shoving.pop(shoving.index(rand.choice(shoving)))
                    if attempt not in bowl:
                        bowl[add_on.index(slot)] = attempt
        # print(bowl, 'current')
    return bowl


def inheritance(prev_gen):
    inherited = [[], [], []]
    for outcome in prev_gen:
        game = deduction(mixer(prev_gen))
        if win_checker(game, 2) == 'win':
            inherited[0].append(game)
        elif win_checker(game, 1) == 'win':
            inherited[1].append(game)
        else:
            inherited[2].append(game)
    return inherited


gen = []
for match in range(1000):
    blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    board = [[], [], [], [], [], [], [], [], []]
    counter = 0
    for position in board:
        board[board.index(position)] = blocks.pop(blocks.index(rand.choice(blocks)))
        result = win_checker(board, counter)
        if result:
            if result == 'win':
                population[counter % 2].append(board)
                break
            elif result == 'draw':
                population[2].append(board)
                break
        counter += 1
    gen.append(board)

gen0 = inheritance(gen)
for g in gen0:
    print(g)
