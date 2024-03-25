import random as rand
from openpyxl import Workbook
import numpy as np

# can the comp figure this out itself?
# tactical hot spots?
# why? why does it need the optimals?
# balancing count

wb = Workbook()
ws = wb.active


def all_possible_tactics():
    wins = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
            ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
            ['a', 'e', 'i'], ['c', 'e', 'g']]
    tactics = []
    for win in wins:
        for win_ind in range(wins.index(win) + 1, len(wins)):
            temp_tac = []
            tact_ava = False
            for block in win:
                if block in wins[win_ind]:
                    tact_ava = True
                    break
            if tact_ava:
                for block in win:
                    # temp_tac = np.append(temp_tac, block)
                    temp_tac.append(block)
                for block in wins[win_ind]:
                    if block not in temp_tac:
                        temp_tac.append(block)
                        # temp_tac = np.append(temp_tac, block)
                    else:
                        temp_tac.insert(0, [block])
                        # temp_tac = np.insert(temp_tac, [0], [block])
            if len(temp_tac):
                tactics.append(temp_tac)
    # solution creating
    existing = []
    li = []
    for tactic in tactics:
        li.append(tactic[0])
        if tactic[0] not in existing:
            existing.append(tactic[0])
    tactics_z = []
    for element in existing:
        goin_in2_l = [element]
        for tactic in tactics:
            if tactic[0] == element:
                for block in tactic[1:]:
                    if block not in goin_in2_l:
                        goin_in2_l.append(block)
        tactics_z.append(goin_in2_l)
    options = {}
    for option in existing:
        for item in tactics_z:
            if item[0] == option:
                options.update({f'{option}': item})
    return options


print(all_possible_tactics())
