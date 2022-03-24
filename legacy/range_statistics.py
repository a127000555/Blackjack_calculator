import enum
import numpy as np
lose_msg = ['Player_Lose','Player_Lose_DD', 'Player_Burst']
win_msg = ['Player_5_win', 'Dealer_Burst', 'Dealer_Burst_DD', 'Black_Jack', 'Player_Win', 'Player_Win_DD']
draw_msg = ['Draw', 'Draw_DD']


def halves(card_num):
    # 2 3 4 5 6 : +1
    # 7 8 9 : +0
    # A 10 J Q K : -1
    strategy = {
        1: -1,
        2: 0.5,
        3: 1,
        4: 1,
        5: 1.5,
        6: 1,
        7: 0.5,
        8: 0,
        9: -0.5,
        10: -1,
    }
    tot = 0
    for idx, remain in enumerate(card_num):
        tot += strategy[idx+1] * remain
    # print(tot, card_num)
    score = tot * 52 / sum(card_num)
    # print(score)
    return score

def cal_score(card_num, N):
    # 2 3 4 5 6 : +1
    # 7 8 9 : +0
    # A 10 J Q K : -1
    x = (sum(card_num[1:6]) - card_num[-1] - card_num[0]) * -1
    return x * 52 / sum(card_num)

rate_table = np.zeros([16, 3])
iter = 0
for row in open('record.txt'):
    iter += 1
    # print("ding")
    card_num, status = row.strip().split()
    card_num = list(map(int, card_num.split('/')))
    # score = cal_score(card_num, 6)
    score = halves(card_num)

    result = 0 if status in lose_msg else 1 if status in draw_msg else 2
    if result == 2:
        assert status in win_msg
    # -4 ~ 4 
    block_id = min(max(int((score + 4) * 2), 0), 15)
    rate_table[block_id][result] += 1
    if iter == 1000:
        break
# print(rate_table / np.sum(rate_table, axis=1, keepdims=True))
for i, row in enumerate(rate_table):
    if sum(row) > 0:
        print(f"Range {i*0.5-4:4.1f} ~ {(i+1)*0.5-4:4.1f}: ({'%3d'%sum(row)}) ", end='')
        print(" ".join(['%6.2f%%' % (cell*100/sum(row)) for cell in row]))

total_rate = np.sum(rate_table, axis=0)
print(total_rate / np.sum(total_rate))
print(np.sum(total_rate))