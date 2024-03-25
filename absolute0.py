import random as rand
from openpyxl import Workbook
import xlrd
import copy

location1 = 'C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\bf0.xlsx'
location2 = 'C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\bf1.xlsx'
location3 = 'C:\\Users\\Dell\\Desktop\\Academic\\Comp_Sci\\SRP\\data\\bf2.xlsx'

wb1 = Workbook()
ws = wb1.active

# the reason learning from ideals did not work is because it did not remove the failied ties
wins = (['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
        ['a', 'd', 'g'], ['b', 'e', 'h'], ['c', 'f', 'i'],
        ['a', 'e', 'i'], ['c', 'e', 'g'])


def reducing(loc=None, lvl2=None):
    if not loc:
        loc = input('path: ')
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    winning_x = []
    winning_o = []
    draw_counts = []
    lists_of_plays = [winning_x, winning_o, draw_counts]
    rows_to_do = [1, 2, 3]
    for r in rows_to_do:
        if not sheet.cell_value(2, r):
            continue
        for combo in range(int(sheet.cell_value(r, 4)) - 1):
            com = sheet.cell_value(combo + 1, r)
            if lvl2:
                com = com.replace('{', '').replace('}', '').replace("'x': ", '').replace("'o': ", '')
            com = com[2:-2].replace("'", '').replace(', ', '').split('][')
            # comb = [[list(com[0])], [list(com[1])]]
            comb = [[], []]
            for block in com[0]:
                comb[0].append(block)
            for block in com[1]:
                comb[1].append(block)
            if comb not in lists_of_plays[rows_to_do.index(r)]:  # do a for loop checking if there are ones dif order
                lists_of_plays[rows_to_do.index(r)].append(comb)
    return lists_of_plays


def combining(list1, list2, list3):
    combined = []
    lists = [list1, list2, list3]
    indexes = (0, 1, 2)
    for ind in indexes:
        temp_list = []
        for list_ in lists:
            for combo in list_[ind]:
                if combo not in temp_list:
                    temp_list.append(combo)
        combined.append(temp_list)
    return combined


def ideal(endings, ind):
    ideal_plays = [[], []]
    ties = endings[ind]
    for tie in ties:
        for side in tie:
            ideal_plays[tie.index(side)].append(side)
    return ideal_plays


# print('Calculation Function Load Up: Complete \nNow Loading: Game Calculations')
# reduced_info = combining(reducing(location1), reducing(location2), reducing(location3))
# combine_x = tuple(ideal(reduced_info, 0))
# print('Calculated: 33.33%')
# combine_o = tuple(ideal(reduced_info, 1))
# print('Calculated: 66.66%')
# combine_t = tuple(ideal(reduced_info, 2))
# print('Calculated: 99.99%')


def win_checker(side):
    if side == x_blocks:
        side = x_blocks['x']
    else:
        side = o_blocks['o']
    for win in wins:
        w_c = 0
        for block in side:
            if block in win:
                w_c += 1
            if w_c > 2:
                return 'win'
    if not blocks:
        return 'tie'


def brute_force(side, other):
    if side == x_blocks:
        other = other['o']
        other_key = 1
        combine = o_won
    else:
        other = other['x']
        other_key = 0
        combine = x_won
    prevent = []
    for check in combine:
        checking = check[other_key]
        ap = True
        for block in other:
            if block not in checking:
                ap = False
                break
        if ap:
            prevent.append(checking)
    while prevent:
        attempt = rand.choice(prevent)
        att = copy.copy(attempt)
        while attempt:
            block = rand.choice(attempt)
            if block in blocks:
                return [block, att]
            else:
                attempt.remove(block)
        prevent.remove(attempt)
    return


def placing(side, other):
    if side == x_blocks:
        side_key = 'x'
    else:
        side_key = 'o'
    ava = informed(side, other)
    prev = brute_force(side, other)
    if ava:
        if len(ava) > 1:
            print('ava')
            side[side_key].append(blocks.pop(blocks.index(ava[0])))
            return ava[1]
    if prev:
        if len(prev) > 1:
            print('prev')
            side[side_key].append(blocks.pop(blocks.index(prev[0])))
            return prev[1]
    if blocks:
        side[side_key].append(blocks.pop(blocks.index(rand.choice(blocks))))
        return
    return


def informed(side, other):
    if side == x_blocks:
        side_ind = 0
        other_ind = 1
        side_key = 'x'
        other = other['o']
        alpha = copy.copy(x_won)
        omega = copy.copy(successes)
    else:
        side_ind = 1
        other_ind = 0
        side_key = 'o'
        other = other['x']
        alpha = copy.copy(o_won)
        omega = copy.copy(successes)
    total_comb = [alpha, omega]
    for priority in total_comb:
        while priority:
            selected = priority.pop(priority.index(rand.choice(priority)))
            similar = True
            for block in side[side_key]:
                if len(selected[side_ind]) < len(side[side_key]):
                    similar = False
                    break
                if block != selected[side_ind][side[side_key].index(block)]:
                    similar = False
                    break
                # print('bug testing')
            if similar:
                for block in other:
                    if len(selected[side_ind]) < len(side[side_key]):
                        similar = False
                        break
                    if block != selected[other_ind][other.index(block)]:
                        similar = False
                        break
                    # print('bug catching')
            if similar and selected:
                sel = copy.copy(selected)
                while selected[side_ind]:
                    ap = rand.choice(selected[side_ind])
                    if ap in blocks:
                        return [ap, sel]
                    else:
                        selected[side_ind].remove(ap)
    return


x_won = []
o_won = []
draws = []
o_success = [[], []]
x_success = [[], []]
successes = []
x_w = 0
o_w = 0
draw = 0
every_10 = []
every_100 = []
x_using = []
o_using = []
match_counts = int(input('Match count: '))
for match in range(match_counts):
    print(match)
    blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    x_blocks = {'x': []}
    o_blocks = {'o': []}
    x_blocks['x'].append(blocks.pop(blocks.index(rand.choice(blocks))))
    print(x_blocks, o_blocks)
    ongoing = True

    while ongoing:
        turn = 1
        if turn % 2:
            side_ = o_blocks
            other_ = x_blocks
            using = o_using
            won = o_won
            wc = o_w
            success = o_success
            other_using = x_using
            other_won = x_won
        else:
            print(turn)
            side_ = x_blocks
            other_ = o_blocks
            using = x_using
            won = x_won
            wc = x_w
            success = x_success
            other_using = o_using
            other_won = o_won
        current_play = placing(side_, other_)
        using.append(current_play)
        print(side_)
        if win_checker(side_) == 'win':
            print('win', x_blocks, o_blocks)
            if [x_blocks, o_blocks] not in won:
                success[0].append(x_blocks['x'])
                success[1].append(o_blocks['o'])
            won.append([x_blocks, o_blocks])
            wc += 1
            if using in won:
                won.remove(using)
            if using in successes:
                successes.remove(using)
            ongoing = False
            break
        print(x_blocks, o_blocks)
        if not blocks and win_checker(x_blocks) != 'win' and win_checker(o_blocks) != 'win':
            if [x_blocks, o_blocks] not in draws:
                print('draw', x_blocks, o_blocks)
                successes.append([x_blocks['x'], o_blocks['o']])
            draws.append([x_blocks, o_blocks])
            draw += 1
            ongoing = False
            break
        turn += 1

    if not (match + 1) % 10:
        every_10.append([x_w, o_w, draw])
        if not (match + 1) % 110 and not every_100:
            every_100.append([x_w, o_w, draw])
        if not (match + 1) % 110 and every_100:
            every_100.append([(x_w - every_10[-11][0]), (o_w - every_10[-11][1]), (draw - every_10[-11][2])])
        if not (match + 1) % 1000:
            print(f'{(match + 1) * 100 / match_counts}%')

blocks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
x_blocks = {'x': []}
o_blocks = {'o': []}
x_blocks['x'].append(input(blocks))
ongoing = True
while ongoing:
    placing(o_blocks, x_blocks)
    if win_checker(o_blocks) == 'win':
        if [x_blocks, o_blocks] not in o_success:
            o_won.append([x_blocks['x'], o_blocks['o']])
        o_success.append([x_blocks, o_blocks])
        o_w += 1
        ongoing = False
        break
    x_blocks['x'].append(input(blocks))
    if win_checker(x_blocks) == 'win':
        if [x_blocks, o_blocks] not in x_success:
            x_won.append([x_blocks['x'], o_blocks['o']])
        x_success.append([x_blocks, o_blocks])
        x_w += 1
        ongoing = False
        break
    if not blocks and win_checker(x_blocks) != 'win' and win_checker(o_blocks) != 'win':
        if [x_blocks, o_blocks] not in draws:
            successes.append([x_blocks['x'], o_blocks['o']])
        successes.append([x_blocks, o_blocks])
        draw += 1
        ongoing = False
