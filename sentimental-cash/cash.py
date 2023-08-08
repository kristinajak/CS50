from cs50 import get_float

# Asking for user input
while True:
    f = get_float("Amount: ")
    if f > 0:
        break

cnt = round(f * 100)
coins = 0

# Number of quarters
while (cnt >= 25):
    cnt = cnt - 25
    coins += 1

# Number of dimes
while (cnt >= 10):
    cnt = cnt - 10
    coins += 1

# Number of nickels
while (cnt >= 5):
    cnt = cnt - 5
    coins += 1

# Number of pennies
while (cnt >= 1):
    cnt = cnt - 1
    coins += 1

print(coins)