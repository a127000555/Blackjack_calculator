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
def halves(card_num, money):
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
    if 0.5 <= score <= 2.4:
        return 10
    return 1
def hi_lo(card_num, money):
    strategy = {
        1: -1,
        2: 1,
        3: 1,
        4: 1,
        5: 1,
        6: 1,
        7: 0,
        8: 0,
        9: 0,
        10: -1,
    }
    tot = 0
    for idx, remain in enumerate(card_num):
        tot += strategy[idx+1] * remain
    print(tot, card_num)
    score = tot * 52 / sum(card_num)
    print(score)
    exit()
    if 0.5 <= score <= 2.4:
        return 5
    return 1

'''
All bet 1 after 1000 rounds: 124.5
'''

dd_times = 0
rr = np.zeros([3])
money = 150
money1 = money
money2 = money
iter = 0

money_history = [money]
delta_history = []

for row in open('record.txt'):
    iter += 1
    if iter < 1000:
        continue
    card_num, status = row.strip().split()
    card_num = list(map(int, card_num.split('/')))
    result = result_table[status]
    if result < 0:
        rr[0] += 1
    elif result == 0:
        rr[1] += 1
    else:
        rr[2] += 1

    if status[-2:] == 'DD':
        dd_times += 1

    # if len(delta_history) > 1 and delta_history[-1] < 0:
    #     last_lost = -delta_history[-1]
    #     bet = min(32, max(1, last_lost)) * 2 * hi_lo(card_num, money)
    # else:
    bet = hi_lo(card_num, money)
    # print(bet * result)
    money += bet * result
    money_history.append(money)
    delta_history.append(bet * result)

    # if money < 0:
    #     print("Backrupt.")
    #     break

print(f"Remain {money} after {iter} tests.")
print(f"Range: {min(money_history), max(money_history)}")
print(rr / np.sum(rr))
print(f"DD ratio: {dd_times / np.sum(rr) * 100: 4.2f}%")
plt.plot(money_history, color='blue')
plt.plot([150] * len(money_history), color='green')
plt.show()


