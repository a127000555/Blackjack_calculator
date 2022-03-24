import numpy as np

def get_pts(now_cards):
    cur_pts = sum(now_cards)
    if 1 in now_cards and cur_pts + 10 <= 21:
        return cur_pts + 10
    else:
        return cur_pts

def cards_to_table(now_cards):
    # Prob Table: Change cards number to prob table that 
    # means [<=16, 17, 18, 19, 20, 21, >=22]
    cur_pts = get_pts(now_cards)
    prob_table = np.zeros([7], dtype=float)
    prob_table[max(16, min(22, cur_pts)) - 16] = 1
    return prob_table

dealer_mem = {}
def dealer_rec(mem, now_cards, card_num, dealer_no_T=False):
    global dealer_mem
    key2 = tuple([1 in now_cards, sum(now_cards)] + card_num.tolist())
    now_cards = sorted(now_cards)
    # Record to memory to save the time.
    if key2 not in dealer_mem:
        cur_pts = sum(now_cards)
        # If dealer has Ace, we'll try to add 10. And if the current points >= 17
        # We'll just return the results.
        if 17 <= cur_pts or (1 in now_cards and 17 <= cur_pts + 10 <= 21):
            return cards_to_table(now_cards)
        else:

            prob_table = np.zeros([7], dtype=float)
            if dealer_no_T:
                now_total_cards = sum(card_num[:-1])
                for choose in range(9):
                    if card_num[choose] >= 1:
                        cur_prob = card_num[choose] / now_total_cards
                        card_num[choose] -= 1
                        prob_table += cur_prob * dealer_rec(mem, now_cards + [choose+1], card_num)
                        card_num[choose] += 1
            else:
                now_total_cards = sum(card_num)
                for choose in range(10):
                    if card_num[choose] >= 1:
                        cur_prob = card_num[choose] / now_total_cards
                        card_num[choose] -= 1
                        prob_table += cur_prob * dealer_rec(mem, now_cards + [choose+1], card_num)
                        card_num[choose] += 1
        dealer_mem[key2] = prob_table
    return dealer_mem[key2]

    
def win_rate_calculate(dealer, player):
    prob = np.array([0, 0, 0]).astype(float)
    for i in range(6):
        for j in range(6):
            cur_prob = dealer[i] * player[j]
            prob += cur_prob * np.array([i>j, i==j, i<j], dtype=float)
    # Player Burst
    prob[0] += player[-1]
    # Dealer Burst
    prob[2] += sum(player[:-1]) * dealer[-1]
    return prob

# If Hit win rate > Stand, than we hit
def policy(mem, dealer_cards, now_cards, card_num, only_1hit=False, dealer_ace_rule=False):
    now_cards = sorted(now_cards)
    if tuple(now_cards) in mem:
        return mem[tuple(now_cards)]
    # Dealer take Ace, and ensure the blocked card is not T.
    dealer_no_T = dealer_ace_rule and (len(dealer_cards) == 1 and dealer_cards[0] == 1)
    # calculate hit rate
    hit_rate = np.zeros([3])
    for choose in range(10):
        next_card_prob = card_num[choose] / sum(card_num)
        if card_num[choose] >= 1:
            # Hit and burst: Do nothing
            if get_pts(now_cards + [choose+1]) > 21:
                hit_rate[0] += next_card_prob
            # Get 5 cards will be counted as winner.
            elif len(now_cards) == 4:
                hit_rate[2] += next_card_prob
            else:
                # Try to get next policy
                card_num[choose] -= 1
                if only_1hit:
                    # Special Rules for Double Down
                    dealer_prob_table = dealer_rec({}, dealer_cards, card_num, dealer_no_T)
                    player_prob_table = cards_to_table(now_cards + [choose+1])
                    hit_rate += next_card_prob * win_rate_calculate(dealer_prob_table, player_prob_table)
                else:
                    next_stand_rate, next_hit_rate = policy(mem, dealer_cards, now_cards + [choose+1], card_num, dealer_ace_rule=dealer_ace_rule)
                    # Calculate the EV after next step
                    next_stand_ev = next_stand_rate[2] - next_stand_rate[0]
                    next_hit_ev = next_hit_rate[2] - next_hit_rate[0]
                    if next_stand_ev > next_hit_ev:
                        hit_rate += next_card_prob * next_stand_rate
                    else:
                        hit_rate += next_card_prob * next_hit_rate
                    
                # Recover the status
                card_num[choose] += 1
    # calculate stand rate
    dealer_prob_table = dealer_rec({}, dealer_cards, card_num, dealer_no_T)
    player_prob_table = cards_to_table(now_cards)
    stand_win_rate = win_rate_calculate(dealer_prob_table, player_prob_table)
    mem[tuple(now_cards)] = np.array([stand_win_rate, hit_rate])
    return mem[tuple(now_cards)]


def get_card_num(*ll):
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    for li in ll:
        for i in li:
            card_num[i-1] -= 1
    return card_num

def calculate_initial_EV(card_num):
    mem = {}
    ev = 0
    for player_known in [ (i+1, j+1) for i in range(10) for j in range(i, 10)]:
        # Check if valid
        if player_known[0] == player_known[1] and card_num[player_known[0]-1] <= 1:
            continue
        elif card_num[player_known[0]-1] == 0 or card_num[player_known[1]-1] <= 0:
            continue
        # Calculate Probibility
        if player_known[0] == player_known[1]:
            prob = card_num[player_known[0]-1] * (card_num[player_known[1]-1] - 1)
        else:
            prob = 2 * card_num[player_known[0]-1] * card_num[player_known[1]-1]
        prob /= sum(card_num) * (sum(card_num)-1)
        # Effect in card_num
        card_num[player_known[0]-1] -= 1
        card_num[player_known[1]-1] -= 1
        # Calculate EV
        stand_rate, hit_rate = policy(mem, [], player_known, card_num, dealer_ace_rule=True)
        stand_ev, hit_ev = (stand_rate[2] - stand_rate[0]), (hit_rate[2] - hit_rate[0])
        best_ev = max(stand_ev, hit_ev)
        # Black jack rule: EV * 1.5
        if get_pts(player_known) == 21:
            dealer_bj_prob = 2 * card_num[0] * card_num[-1]
            dealer_bj_prob /= sum(card_num) * (sum(card_num) - 1)
            best_ev = (1 - dealer_bj_prob) * 1.5
        # Double Down rule: EV * 2
        if 9 <= get_pts(player_known) <= 11:
            _, dd_rate = policy({}, [], player_known, card_num, only_1hit=True, dealer_ace_rule=True)
            dd_ev = (dd_rate[2] - dd_rate[0]) * 2
            best_ev = max(best_ev, dd_ev)
        # Split rule: EV * 2
        if player_known[0] == player_known[1]:
            _, split_rate = policy(mem, [], player_known[:1], card_num, dealer_ace_rule=True)
            split_ev = (split_rate[2] - split_rate[0]) * 2
            best_ev = max(best_ev, split_ev)
        # Add EV
        ev += prob * best_ev
        # Recover card_num
        card_num[player_known[0]-1] += 1
        card_num[player_known[1]-1] += 1
        print("%d, %d, %.6f" % (*player_known, prob))
    return ev

if __name__ == '__main__':
    
    N = 6
    card_num = np.array([ 4*N ] * 9 + [ 4*4*N ])
    print(card_num)
    # print(dealer_rec({}, [6], card_num))
    # print(policy({}, [6], [2, 3], card_num))
    print(calculate_initial_EV(card_num))
    print(policy({}, [1], [1], card_num, dealer_ace_rule=True))
    exit()
    player_known = []
    other_known = [2, 3, 4, 5] * 2
    dealer_known = []
    print(calculate_initial_EV(get_card_num(other_known)))

    mem = {}
    print("-----------23456789TA")
    for player_known in [[3, 5], [4, 5], [3, 7], [5, 6], [5, 7], [6, 7], [6, 8], [7, 8], [7 ,9], [10, 7]]:
        print(f"{player_known[0]:2d} {player_known[1]:2d}  {get_pts(player_known):2d}| ", end='')
        for dealer_known in [ [i+1] for i in range(1, 10) ] + [[1]]:
            card_num = get_card_num(player_known, dealer_known)
            stand_rate, hit_rate = policy(mem, dealer_known, player_known, card_num, dealer_ace_rule=True)
            _, dd_rate = policy({}, dealer_known, player_known, card_num, only_1hit=True, dealer_ace_rule=False)
            stand_ev = stand_rate[2] - stand_rate[0]
            hit_ev = hit_rate[2] - hit_rate[0]
            dd_ev = (dd_rate[2] - dd_rate[0]) * 2
            
            if dd_ev > stand_ev and dd_ev > hit_ev:
                print("D", end='')
            elif stand_ev > dd_ev and stand_ev > hit_ev:
                print("S", end='')
            else:
                print("H", end='')
        print()
    print("=" * 5)
    mem = {}
    card_num = get_card_num(other_known, player_known, dealer_known)
    stand_rate, hit_rate = policy(mem, dealer_known, player_known, card_num, dealer_ace_rule=True)
    stand_ev = (stand_rate[2] - stand_rate[0])
    hit_ev = (hit_rate[2] - hit_rate[0])
    policies = [(stand_ev, 'stand'), ((hit_ev), 'hit')]
    if len(player_known) == 2:
        _, dd_rate = policy({}, dealer_known, player_known, card_num, only_1hit=True)        
        dd_ev = (dd_rate[2] - dd_rate[0]) * 2
        policies.append((dd_ev, 'double down'))
        if player_known[0] == player_known[1]:
            _, split_rate = policy(mem, dealer_known, player_known[:1], card_num)
            split_ev = (split_rate[2] - split_rate[0]) * 2
            policies.append((split_ev, 'split'))
    def fmt(r):
        return '|'.join([ f' {c:<9,.3%}' for c in r])

    print('Policy |', '|'.join([ f'{s: ^10}' for s in ["Lose", "Tie", "Win", "EV"]]))
    print('-' * 70)
    print('Stand  |', fmt(stand_rate), "|", '%3.2f' % stand_ev)
    print('Hit    |', fmt(hit_rate), "|", '%3.2f' % hit_ev)
    if len(player_known) == 2:
        print('DD     |', fmt(dd_rate), "|", '%3.2f' % dd_ev)
        if player_known[0] == player_known[1]:
            print('Split  |', fmt(split_rate), "|", '%3.2f' % split_ev)
    policies = sorted(policies, reverse=True)
    print('=' * 70)
    print(f"Best Policy: {policies[0][1]} with EV= {policies[0][0]}")

