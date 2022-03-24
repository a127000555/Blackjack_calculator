import numpy as np
import random
from termcolor import colored
from neil import double_down_rate, policy, get_pts


money = 100

statistics = np.array([0, 0, 0]).astype(float)

# N = 1: 0.506   0.058   0.436   Total 500
def cal_score(card_num, N):
    # 2 3 4 5 6 : +1
    # 7 8 9 : +0
    # A 10 J Q K : -1
    x = (sum(card_num[1:6]) - card_num[-1] - card_num[0])
    return x * 52 / sum(card_num)

f = open("record.txt", 'a')
def record(card_num, result):
    # score = cal_score(card_num)
    print('/'.join(map(str, card_num)), result, file=f)
    f.flush()

def get_bet2(card_num, money):
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
        return 8
    return 1


from Crypto.Random.random import shuffle

def trial(N=6, verbose=True):
    global money
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    cards = (list(range(1, 10)) + [10] * 4) * 4 * N
    shuffle(cards)
    random.shuffle(cards)
    def get_card():
        res = cards[-1]
        card_num[res-1] -= 1
        cards.pop()
        return res
        
    if verbose:
        import sys
        file = sys.stdout
    else:
        file = open('nul', 'w')

    if verbose:
        print()

    round = 0
    while len(cards) > 52 * N * 2 / 3:
        if sum(statistics) != 0:
            for p in (statistics / sum(statistics)):
                print(f"%3.3f" % p, end='   ')
            print("Total", int(sum(statistics)), "Now money: ", money)

        round += 1
        # bet = money / 2
        score = cal_score(card_num, N)
        bet = get_bet2(card_num, money)
        money -= bet

        print(f"="*40, file=file)
        print("{: ^40s}".format(f"Round #{round} - Bet {bet} / Score {cal_score(card_num, N):.3f}"), file=file)
        print(f"-"*40, file=file)

        dealer = [get_card()]
        print(f"Dealer Get  : {dealer[0]}", file=file)
        player = [get_card(), get_card()]

        def print_player(s):
            print("{: >40s}".format(s), file=file)
        def announcement(s, color=None):
            if color:
                print(colored("{: ^40s}".format(s), color), file=file)
            else:
                print("{: ^40s}".format(s), file=file)

        print_player(f"{' '.join(map(str, player))} : Player Get  ")
        is_dd = False

        # Player Decision
        # If Player get black jack, win instantly.
        if 1 in player and 10 in player:
            announcement("Player Win", 'green')
            record(card_num, "Black_Jack")
            money += bet * 2.5
            statistics[2] += 1
            continue
            
        if 1 not in player and 9 <= get_pts(player) <= 11:
            dd_rate = double_down_rate(dealer, player, card_num)
            if dd_rate >= 0.5:
                card = get_card()
                print_player(f"{card} : Player DD   ")
                announcement("Player call Double Down!!", "yellow")
                money -= bet
                player.append(card)
                is_dd = True

        if not is_dd:
            stand, hit = policy(dealer, player, card_num)
            while hit > stand and len(player) < 5:
                card = get_card()
                print_player(f"{card} : Player Hit  ")
                player.append(card)
                if get_pts(player) > 21:
                    print_player("burst")
                    break
                if len(player) == 5:
                    break 
                stand, hit = policy(dealer, player, card_num)

        # If burst, then don't give dealer card.
        if get_pts(player) > 21:
            announcement("Player Lose", 'red')
            statistics[0] += 1
            record(card_num, "Player_Burst")
            continue

        if len(player) == 5:
            announcement("Player Win", 'green')
            record(card_num, "Player_5_win")
            money += bet * 2
            statistics[2] += 1
            continue

        print_player(f"({get_pts(player)}) {' '.join(map(str, player))} : Player Stand")
            
        # Dealer Round
        while get_pts(dealer) < 17:
            card = get_card()
            print(f"Dealer Hit  : {card}", file=file)
            dealer.append(card)
        print(f"Dealer Stand: {' '.join(map(str, dealer))} ({get_pts(dealer)})", file=file)

        # Dealer Burst
        if get_pts(dealer) > 21:
            announcement("Player Win", 'green')
            statistics[2] += 1
            if is_dd:
                money += bet * 4
                record(card_num, "Dealer_Burst_DD")
            else:
                money += bet * 2
                record(card_num, "Dealer_Burst")
            continue
        
        # Race
        if get_pts(dealer) > get_pts(player):
            announcement("Player Lose", 'red')
            statistics[0] += 1
            if is_dd:
                record(card_num, "Player_Lose_DD")
            else:
                record(card_num, "Player_Lose")
        elif get_pts(dealer) == get_pts(player):
            announcement("Draw")
            statistics[1] += 1
            if is_dd:
                money += bet * 2
                record(card_num, "Draw_DD")
            else:
                money += bet * 1
                record(card_num, "Draw")
        else:
            announcement("Player Win", 'green')
            statistics[2] += 1
            if is_dd:
                record(card_num, "Player_Win_DD")
                money += bet * 4
            else:
                record(card_num, "Player_Win")
                money += bet * 2


if __name__ == '__main__':
    for i in range(10000):
        trial(verbose=True)
        print("\n" + f"{'Change Cards': ^30}" + "\n")
