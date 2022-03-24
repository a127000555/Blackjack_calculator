from turtle import color
import matplotlib.pyplot as plt
import numpy as np
result_table = {
    'Player_Lose': -1,
    'Player_Lose_DD': -2,
    'Player_Burst': -1,
    'Player_5_win': 1, 
    'Draw': 0, 
    'Draw_DD': 0, 
    'Dealer_Burst': 1, 
    'Dealer_Burst_DD': 2, 
    'Black_Jack': 1.5, 
    'Player_Win': 1, 
    'Player_Win_DD': 2
}
def halves(card_num, money, L=0, R=2):
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
    score = tot * 52 / sum(card_num)
    if L < score <= R:
        return 5
    return 1
'''
All bet 1 after 1000 rounds: 124.5

'''
def trial(L=0, R=2):
    money = 150
    ite = 0
    for row in open('record.txt'):
        card_num, status = row.strip().split()
        card_num = list(map(int, card_num.split('/')))
        result = result_table[status]

        bet = halves(card_num, money, L, R)
        money += bet * result
        ite += 1
        if ite == 1000:
            break
    return money

best = (0, 0, 0)
for L in np.arange(0, 1, 0.1):
    for R in np.arange(L+0.5, 3, 0.1):
        money = trial(L, R)
        best = max(best, (money, L, R))
        print(money, '%.2f'%L, '%.2f'%R)
        # print(best)
money, L, R = best
print('best', money, '%.2f'%L, '%.2f'%R)
# print(f"Remain {money} after {ite} tests.")
