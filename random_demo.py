import random


# 随机抽取其中几个
picks = []
for _ in range(5):
    pick = random.randint(0, 30000)
    while pick in picks:
        pick = random.randint(0, 30000)
    picks.append(pick)
print(picks)
