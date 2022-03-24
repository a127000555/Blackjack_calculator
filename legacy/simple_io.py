import numpy as np
import msvcrt
import os
import sys
from neil import dealer_rec, policy, double_down_rate

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
    score = tot * 52 / sum(card_num)
    return score
N = 6
other_known = []
player_known = []
dealer_known = []

def help():
    print(f"{' Help ':=^70}")
    print(f"{' [R] : Reset, the dealer shuffle the cards.': <30}")
    print(f"{' [N] : Next Round, clean the dealer and your card.': <30}")
    print(f"{' [C] : Calculate, calculate the win rate.': <30}")
    print(f"{' [D] : Dealer Card, the next card is from dealer.': <30}")
    print(f"{' [P] : Player Card, the next card is from player (You).': <30}")
    print(f"{' [O] : Others, the next card is from dealer.': <30}")
    print(f"{' [Z] : ZZZ, Do nothing, just look the prob.': <30}")
    print(f"{' [X] : Exit the program.': <30}")
    print(f"{' [H] : Show this help message': <30}")
    print(f"{'':=^70}")

help()
def get_key():
    valid_s = '1a234567890tjqk'
    input_char = msvcrt.getch().decode()
    v = valid_s.find(input_char)
    if v == -1:
        return (input_char, -1)
    else:
        return (input_char, max(1 , min(10, v)))
def get_card_num(*ll):
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    for li in ll:
        for i in li:
            card_num[i-1] -= 1
    return card_num

def tos(l):
    return ''.join([ '-A23456789T'[i] for i in l ])

def get_status():
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
    print("Input Keys: ", end='')

last_key = None
while True:
    if last_key is None:
        try:
            input_char = msvcrt.getch().decode()
        except:
            print("You can only input [RCDPOXHZ]")
            continue
    else:
        input_char = last_key
        last_key = None

    if ord(input_char) ==13:
        print()
    else:
        get_status()
        print(f'[{input_char}]', end='')
    sys.stdout.flush()
    if input_char == 'r':
        print("Reset the cards")
        other_known, player_known, dealer_known = [], [], []
    elif input_char == 'n':
        print("Go next round")
        other_known += player_known + dealer_known
        player_known, dealer_known = [], []
        get_status()
    elif input_char in ['d', 'p', 'o']:
        while True:
            k = get_key()
            if k[1] != -1:
                sys.stdout.flush()
                if input_char == 'd':
                    dealer_known.append(k[1])
                elif input_char == 'p':
                    player_known.append(k[1])
                elif input_char == 'o':
                    other_known.append(k[1])
                get_status()
                print(f'[{k[0]}]', end='')
            else:
                last_key = k[0]
                break
    
    elif input_char == 'h':
        help()
    elif input_char == 'x':
        print("Exit the program")
        break
    # Output

    if input_char == 'c':
        print()
        print("Calculated...")
        card_num = get_card_num(dealer_known, player_known, other_known)
        dealer_prob_table = dealer_rec(dealer_known, card_num)
        stand_rate, hit_rate = policy(dealer_known, player_known, card_num)        
        dd_rate = double_down_rate(dealer_known, player_known, card_num)
        print("        Stand Win Rate :", '%.3f' % stand_rate)
        print("          Hit Win Rate :", '%.3f' % hit_rate)
        print("DD / Hit Once Win Rate :", '%.3f' % dd_rate)
        if len(player_known) and dd_rate > 0.5:
            print("Best Policy: Double Down")
        elif hit_rate > stand_rate:
            print("Best Policy: Hit")
        else:
            print("Best Policy: Stand")
    print()
    sys.stdout.flush()
    
exit()

