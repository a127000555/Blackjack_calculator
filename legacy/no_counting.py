import numpy as np
from random import randint

def count(cards):
    x = sum(cards)
    if 17 <= x:
        return min(22, x)
    elif 1 in cards and 17 <= 10+x <= 21:
        return 10+x
    else:
        return x

def test(initial):
    cards = [initial]
    while count(cards) < 17:
        cards.append(min(10, randint(1, 13)))
    return count(cards)

from neil import show_prob_table

for s in ['-', '17', '18', '19', '20', '21', '>=22']:
    fmt_s = f"{s: ^10}"
    print(fmt_s, end='|')
print()
L = (len(fmt_s) + 1) * 7
print("-" * L)
for i in range(16, 17):
    N = 1000000
    cnt = np.array([0, 0, 0, 0, 0, 0]).astype(float)
    for _ in range(N):
        cnt[test(i)-17] += 1
    cnt /= N
    L = (len(fmt_s) + 1) * 7

    print(f'{i: ^10}', end="|")
    for i, p in enumerate(cnt):
        tmp = f"{p*100:6.2f}%"
        print(f'{tmp: ^10}', end="|")
    print()
    # print(cnt)
    # exit()