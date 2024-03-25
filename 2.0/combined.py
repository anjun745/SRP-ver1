import random as rand

# learning from mistakes
ideals = []
prevention = []
blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
board = [[], [], [], [], [], [], [], [], []]
wins = (['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g'])


def win_checker(game):
    match_length = 0
    checking = []
    for slot in game:
        if slot:
            match_length += 1
        else:
            break
    if match_length % 2:
        for i in range(len(game)):
            if not i % 2:
                checking.append(game[i])
    else:
        for i in range(len(game)):
            if i % 2:
                checking.append(game[i])
    for win in wins:
        w_c = 0
        for block in checking:
            if block in win:
                w_c += 1
            if w_c > 2:
                return 'win'
    for placed in game[::-1]:
        if not placed:
            return
    return 'draw'


def dfi(state):
    tmr = []
    similar = ideals.copy()
    for mapping in similar:
        if not state[0]:
            return
        for slot in state:
            if slot:
                if state[state.index(slot)] != mapping[state.index(slot)]:
                    tmr.append(state)
                    break
            else:
                break
    for t in tmr:
        similar.remove(t)
    try:
        return rand.choice(similar)
    except IndexError:
        return


def remover(end):
    if end in ideals:
        ideals.remove(end)
    if end not in prevention:
        prevention.append(end)
    return


def finisher(state):
    """finish the game/prevention"""
    x_blocks = []
    o_blocks = []
    for slot in state:
        if slot:
            if state.index(slot) % 2:
                # starting from index 1
                o_blocks.append(slot)
            else:
                x_blocks.append(slot)
        else:
            break
    if len(x_blocks) == len(o_blocks):
        side = x_blocks
        other = o_blocks
    else:
        side = o_blocks
        other = x_blocks
    for win in wins:
        win_counter = 0
        win_copy = win.copy()
        for block in side:
            if block in win_copy:
                win_counter += 1
                win_copy.remove(block)
        if win_counter > 1 and win_copy[0] in blocks:
            return win_copy[0]
        for block in other:
            if block in win_copy:
                win_counter += 1
                win_copy.remove(block)+
        if win_counter > 1 and win_copy[0] in blocks:
            return win_copy[0]
    return


for _ in range(1):
    blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    board = [[], [], [], [], [], [], [], [], []]
    m_c = 0
    for move in board:
        m_c += 1
        finishing = finisher(board)
        if finishing:
            board[board.index(move)] = finishing
        if m_c == 1:
            mimicking = dfi(board)

