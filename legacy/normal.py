from Crypto.Random.random import randint
original = 150
history = [original]
for _ in range(200000):
    M = 1000
    d = randint(0, M)
    if d <= M//2:
        original += 1
    else:
        original -= 1
    # print(d)
    # original += d
    history.append(original)

import matplotlib.pyplot as plt 
plt.plot(history, color='red')
plt.plot([150] * len(history), color='green')
plt.show()
