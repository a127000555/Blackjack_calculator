import numpy as np
import matplotlib.pyplot as plt

card_nums = []
evs = []
hi_los = []
N = 6
def get_hi_lo(card_num):
    init_cards = [4 * N] * 9 + [4 * 4 * N]
    showed = np.array(init_cards) - np.array(card_num)
    # corr: 0.6859150925763093, err: 0.41709816575767866
    hi_lo = [None, -1, 1, 1, 1, 1, 1, 0, 0, 0, -1]
    # corr: 0.5223415570880187, err: 0.5727763466148592
    hi_opt_1 = [None, 0, 0, 1, 1, 1, 1, 0, 0, 0, -1]
    # corr: 0.5107693441602528, err: 0.5821934832928134
    hi_opt_2 = [None, 0, 1, 1, 2, 2, 1, 1, 0, 0, -2]
    # corr: 0.6735441902737693, err: 0.4303453353175284
    ko = [None, -1, 1, 1, 1, 1, 1, 1, 0, 0, -1]
    # corr: 0.5114966958127013, err: 0.5816077985955644
    omega_2 = [None, 0, 1, 1, 2, 2, 2, 1, 0, -1, -2]
    # corr: 0.7446468520350055, err: 0.35091688114183084
    halves = [None, -1, 0.5, 1, 1, 1.5, 1, 0.5, 0, -0.5, -1]
    # corr: 0.6539164576749429, err: 0.45086864042668473
    zen_cnt = [None, -1, 1, 1, 2, 2, 2, 1, 0, 0, -2]
    # corr: 0.874585236589017, err: 0.18518651937384117
    neil_1 = [None, -4, 1.6, 1.6, 1.6, 1.6, 1.6, 0, 0, 0, -1]
    # corr: 0.889496052712806, err: 0.16446719823613418
    neil_2 = [None, -4, 1, 1, 1, 2, 3, 0, 0, 0, -1]
    # corr: 0.9255054473855043, err: 0.11298603840872554
    neil_3 = [None, -4, 1, 1, 1, 3, 2, 0, 0, 0, -1]


    strategy = neil_3
    assert abs(sum(strategy[1:]) + strategy[-1] * 3 - 0) < 1e-8
    score = 0
    for idx, showed_num in enumerate(showed):
        score += strategy[idx+1] * showed_num
    numbers_showed = sum(showed)
    numbers_remains = sum(card_num)
    return score

l, w = 0, 0
for row in open('record_ev.txt', 'r'):
    # print(row)
    card_num, ev, hi_lo = row.strip().split()
    card_num = tuple( map(int, card_num.split('/') ))
    hi_lo = get_hi_lo(card_num)
    card_nums.append(card_num)
    evs.append(float(ev))
    hi_los.append(float(hi_lo))

X = np.array(hi_los).reshape([-1, 1])
X = np.concatenate([np.ones_like(X), X], axis=1)
Y = np.array(evs)
w = np.linalg.pinv(X) @ Y
corr = np.corrcoef(evs, hi_los)[0, 1] 
print("lin_reg weight :", w)
print("Correlation :", corr)
print("Mean Square Error :", np.sum((X@w - Y)**2))
# exit()
if True:
    plt.scatter(hi_los, evs, marker='x')
    plt.xlabel("Hi-Lo")
    plt.ylabel("Ev")
    plt.title(f"Corr = {corr:.4f}")
    l_bound, r_bound = min(hi_los), max(hi_los)
    plt.plot([l_bound, r_bound], [w[0] + w[1]*l_bound, w[0] + w[1]*r_bound], c='red')
    plt.plot([l_bound, r_bound], [0, 0], c='orange')
    plt.plot([0, 0], [min(evs), max(evs)], c='orange')
    plt.show()

errs = []
for c, x, y in zip(card_nums, hi_los, evs):
    y_pred = w[0] + w[1] * x
    err = (y - y_pred) ** 2
    errs.append((err, c, x, y))
errs = sorted(errs, reverse=True)
if False:
    original = np.array([4 * N] * 9 + [4 * 4 * N] )
    for err, c, hi_lo, ev in errs[:10]:
        y_pred = w[0] + w[1] * hi_lo
        c = np.array(c)
        print(err, original-c, hi_lo, y_pred, ev)
