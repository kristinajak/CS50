from cs50 import get_int

# Asking the user for input
while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for i in range(n):
    # Printing spaces
    for j in range(n-1-i):
        print(" ", end="")
    # Printing hashes
    for k in range(i+1):
        print("#", end="")
    print()