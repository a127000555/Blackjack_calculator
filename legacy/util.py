
def show_prob_table(ary, title="Dealer Prob"):
    print(title)
    for s in ['<=16', '17', '18', '19', '20', '21', '>=22']:
        fmt_s = f"{s: ^10}"
        print(fmt_s, end='|')
    print()
    L = (len(fmt_s) + 1) * 7
    print("-" * L)
    for i, p in enumerate(ary):
        tmp = f"{p*100:6.2f}%"
        print(f'{tmp: ^10}', end="|")
    print()

