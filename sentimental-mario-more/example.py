from cs50 import get_int

# Asking the user of input
n = get_int("Height: ")

# Printing that many lines
for i in range(n):

    # Printing spaces
    for j in range(i):
        print(" ", end="")

    # Printing hashes
    for k in range(n*2-(2*i+1)):
        print("#", end="")

    print()

