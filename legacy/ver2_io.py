import numpy as np
from neil import policy
import os

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

def tos(l):
    return ''.join([ '-A23456789T'[i] for i in l ])

def input_2_num(input_char):
    valid_s = '1a234567890tjqk'
    v = valid_s.find(input_char)
    if v == -1:
        raise Exception(f"Input error: {input_char}")
    else:
        return max(1 , min(10, v))

def print_status():
    os.system("cls")
    print(f"Dealer     : {tos(dealer_known)}")
    print(f"Player     : {tos(player_known)}")
    print(f"Now Showed : {tos(other_known)}")
    print("=" * 40)
    card_num = get_card_num(dealer_known, player_known, other_known)
    card_prob = card_num / np.sum(card_num)
    for prob, symbol in  zip(card_prob, 'A23456789T'):
        print(f"{symbol}: {prob*100:.1f}%", end=' ')
    print()
    print(f"Hi-Lo Value: {hi_lo(card_num)}")
    print()


def get_card_num(*ll):
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    for li in ll:
        for i in li:
            card_num[i-1] -= 1
    return card_num

def print_policy(dealer_known, player_known, other_known):
    mem = {}
    card_num = get_card_num(other_known, player_known, dealer_known)
    stand_rate, hit_rate = policy(mem, dealer_known, player_known, card_num, dealer_ace_rule=True)
    stand_ev = (stand_rate[2] - stand_rate[0])
    hit_ev = (hit_rate[2] - hit_rate[0])
    policies = [(stand_ev, 'stand'), ((hit_ev), 'hit')]
    if len(player_known) == 2:
        _, dd_rate = policy({}, dealer_known, player_known, card_num, only_1hit=True, dealer_ace_rule=True)        
        dd_ev = (dd_rate[2] - dd_rate[0]) * 2
        policies.append((dd_ev, 'double down'))
        if player_known[0] == player_known[1]:
            # Split rule
            p = player_known[0]
            # card_num[p-1] -= 1
            print(card_num)
            _, split_rate = policy({}, dealer_known, [p], card_num, dealer_ace_rule=True)
            print(split_rate, split_rate[2] - split_rate[0])
            # card_num[p-1] += 1
            split_ev = (split_rate[2] - split_rate[0]) * 2
            policies.append((split_ev, 'split'))
    def fmt(r):
        return '|'.join([ f' {c:<9,.3%}' for c in r])

    print('Policy |', '|'.join([ f'{s: ^10}' for s in ["Lose", "Tie", "Win", "EV"]]))
    print('-' * 70)
    print('Stand  |', fmt(stand_rate), "|", '%3.6f' % stand_ev)
    print('Hit    |', fmt(hit_rate), "|", '%3.6f' % hit_ev)
    if len(player_known) == 2:
        print('DD     |', fmt(dd_rate), "|", '%3.6f' % dd_ev)
        if player_known[0] == player_known[1]:
            wr = split_rate[2] ** 2 + 2 * split_rate[2] * split_rate[1]
            er = split_rate[1] ** 2 + 2 * split_rate[2] * split_rate[0]
            lr = split_rate[0] ** 2 + 2 * split_rate[0] * split_rate[1]
            print('Split  |', fmt([lr, er, wr]), "|", '%3.6f' % split_ev)
    policies = sorted(policies, reverse=True)
    print('=' * 70)
    print(f"Best Policy: {policies[0][1]} with EV= {policies[0][0]}")
# ===================================================================================== #

N = 6
other_known, player_known, dealer_known = [], [], []

print("=" * 70)
print(" [Player's cards] / [Dealer's card] / [Other's cards] : Next Round")
print(" H[cards] : Hit card and get policy and get policy")
print(" O[cards] : Put other cards")
print(" R        : Reset")
print(" Z        : Clean player's cards, this command is for split.")
print("=" * 70)
# 73/5

while True:
    cmd = input().strip()
    needs_calc = False
    if len(cmd.split('/')) == 2:
        cmd += '/'
    if len(cmd.split('/')) == 3:
        player, dealer, other = [ list(map(input_2_num, s.strip())) for s in cmd.split('/') ]
        # Next Round
        other_known += dealer_known + player_known + other
        dealer_known = dealer
        player_known = player
        needs_calc = True
    elif cmd[0].lower() == 'h':
        # Hit
        player_known += list(map(input_2_num, cmd[1:]))
        needs_calc = True
    elif cmd[0].lower() == 'o':
        # Put trash cards
        other_known += list(map(input_2_num, cmd[1:]))
    elif cmd[0].lower() == 'r':
        # Reset the cards
        other_known, player_known, dealer_known = [], [], []
    elif cmd[0].lower() == 'z' or cmd[0].lower() == 's':
        # Split the cards
        player_known = []
    print_status()
    if needs_calc:
        print_policy(dealer_known, player_known, other_known)




# print_status()

