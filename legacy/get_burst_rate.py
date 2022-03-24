import numpy as np
import random

from neil import dealer_rec, show_prob_table
N = 6


result = []
for iter in range(1000):
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    cards = (list(range(1, 10)) + [10] * 4) * 4 * N
    random.shuffle(cards)


    def get_card():
        res = cards[-1]
        card_num[res-1] -= 1
        cards.pop()
        return res

    for _ in range(27 * 6):
        get_card()
    result.append(dealer_rec([], card_num)[-1])
    print(iter, np.mean(np.array(result)) * 100, np.std(np.array(result)) *100)

# 100 28.467751293804522 1.3733228797290185
# 27: 100 28.513068043046335 1.7066345150874493
# print(res)