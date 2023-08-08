from cs50 import get_int

# Asking the user of input
while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

# Printing that many lines
for i in range(n):

    # Printing spaces
    for j in range(n-1-i):
        print(" ", end="")

    # Printing left side hashes
    for k in range(i+1):
        print("#", end="")

    # Printing spaces between
    print("  ", end="")

    # Printing right side hashes
    for s in range(i+1):
        print("#", end="")

    print()

