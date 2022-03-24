from ctypes import *
from os.path import abspath
policy_dll = WinDLL(abspath('policy.dll'))
IntArray10 = c_int16 * 10
policy_dll.calculate_ev.argtypes = [IntArray10]
policy_dll.calculate_ev.restype = c_double

def hi_lo(card_num):
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
    # print(tot, card_num)
    score = -tot * 52 / sum(card_num)
    return score

def get_ev(card_nums):
    p = IntArray10(*card_nums)
    ret = policy_dll.calculate_ev(p)
    return ret


cards_num_set = set()
for row in open('legacy/record.txt', 'r'):
    card_num, game_result = row.strip().split()
    cards_num_set.add(card_num)

import random
cards_num_set = list(cards_num_set)
random.shuffle(cards_num_set)
from multiprocessing import Pool

def work(card_num):
    f = open("record_ev.txt", 'a')
    card_num_l = tuple(map(int, card_num.split('/')))
    print(card_num, get_ev(card_num_l), hi_lo(card_num_l), file=f)
    f.flush()
if __name__ == '__main__':
    p = Pool(8)
    p.map(work, cards_num_set)

# print(cards_num_set)